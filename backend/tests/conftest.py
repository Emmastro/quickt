import asyncio
import uuid

import asyncpg
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.database import Base, get_db
from app.main import app

settings = get_settings()

TEMPLATE_DB = "quickt_test_template"
BASE_URL = settings.database_url.rsplit("/", 1)[0]


async def _admin_conn():
    url = settings.database_url.replace("postgresql+asyncpg://", "")
    parts = url.rsplit("/", 1)
    conn_str = f"postgresql://{parts[0]}/postgres"
    return await asyncpg.connect(conn_str)


async def _setup_template():
    conn = await _admin_conn()
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", TEMPLATE_DB
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{TEMPLATE_DB}"')

        engine = create_async_engine(f"{BASE_URL}/{TEMPLATE_DB}", echo=False)
        async with engine.begin() as c:
            await c.run_sync(Base.metadata.drop_all)
            await c.run_sync(Base.metadata.create_all)
        await engine.dispose()

        await conn.execute(
            f"ALTER DATABASE \"{TEMPLATE_DB}\" WITH is_template = true"
        )
    finally:
        await conn.close()


async def _create_test_db(name: str):
    conn = await _admin_conn()
    try:
        await conn.execute(f'CREATE DATABASE "{name}" TEMPLATE "{TEMPLATE_DB}"')
    finally:
        await conn.close()


async def _drop_test_db(name: str):
    conn = await _admin_conn()
    try:
        await conn.execute(
            f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{name}'"
        )
        await conn.execute(f'DROP DATABASE IF EXISTS "{name}"')
    finally:
        await conn.close()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_template_db():
    await _setup_template()


@pytest_asyncio.fixture
async def db_session():
    test_db = f"quickt_test_{uuid.uuid4().hex[:8]}"
    await _create_test_db(test_db)

    engine = create_async_engine(f"{BASE_URL}/{test_db}", echo=False)
    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_factory() as session:
        yield session

    await engine.dispose()
    await _drop_test_db(test_db)


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()


# ---------- helpers ----------

async def create_user(client, role="customer", **overrides):
    payload = {
        "email": f"{uuid.uuid4().hex[:8]}@quickt.tg",
        "password": "password123",
        "full_name": f"Test {role.title()}",
        "phone": "+22890000000",
        "city": "Lome",
        "role": role,
        **overrides,
    }
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201, resp.text
    return payload


async def login(client, email, password="password123"):
    resp = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text
    tokens = resp.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


async def auth_headers(client, role="customer", **overrides):
    user = await create_user(client, role=role, **overrides)
    return await login(client, user["email"]), user


async def create_agency(client, headers, **overrides):
    payload = {
        "name": f"Agency {uuid.uuid4().hex[:6]}",
        "description": "Test agency",
        "phone": "+22890000099",
        "email": "agency@test.tg",
        "address": "123 Test Street",
        "city": "Lome",
        "region": "Maritime",
        **overrides,
    }
    resp = await client.post("/api/v1/agencies/", json=payload, headers=headers)
    assert resp.status_code == 201, resp.text
    return resp.json()
