from collections.abc import AsyncGenerator

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB as _JSONB
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class JSONBType(sa.types.TypeDecorator):
    """JSONB on PostgreSQL, JSON fallback."""

    impl = sa.JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(_JSONB())
        return dialect.type_descriptor(sa.JSON())


settings = get_settings()


class Base(DeclarativeBase):
    pass


def build_engine(url: str | None = None) -> AsyncEngine:
    target_url = url or settings.database_url
    return create_async_engine(
        target_url,
        echo=not settings.is_production,
        pool_pre_ping=True,
    )


engine = build_engine()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
