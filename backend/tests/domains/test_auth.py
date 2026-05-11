import pytest
from tests.conftest import auth_headers, create_user, login


async def test_register_success(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "new@quickt.tg",
        "password": "password123",
        "full_name": "New User",
        "phone": "+22890111111",
        "city": "Lome",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_register_duplicate_email(client):
    await create_user(client, email="dup@quickt.tg")
    resp = await client.post("/api/v1/auth/register", json={
        "email": "dup@quickt.tg",
        "password": "password123",
        "full_name": "Dup User",
        "phone": "+22890222222",
    })
    assert resp.status_code == 409


async def test_login_success(client):
    await create_user(client, email="login@quickt.tg")
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@quickt.tg",
        "password": "password123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client):
    await create_user(client, email="wrong@quickt.tg")
    resp = await client.post("/api/v1/auth/login", json={
        "email": "wrong@quickt.tg",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


async def test_get_me(client):
    headers, user = await auth_headers(client)
    resp = await client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == user["email"]
    assert data["full_name"] == user["full_name"]


async def test_update_preferences(client):
    headers, _ = await auth_headers(client)
    resp = await client.patch("/api/v1/auth/me", json={
        "full_name": "Updated Name",
        "city": "Kara",
    }, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["full_name"] == "Updated Name"
    assert data["city"] == "Kara"


async def test_refresh_token(client):
    await create_user(client, email="refresh@quickt.tg")
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "refresh@quickt.tg",
        "password": "password123",
    })
    tokens = login_resp.json()
    resp = await client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data


async def test_forgot_password(client):
    await create_user(client, email="forgot@quickt.tg")
    resp = await client.post("/api/v1/auth/forgot-password", json={
        "email": "forgot@quickt.tg",
    })
    assert resp.status_code == 200
    assert "reset link" in resp.json()["message"].lower()


async def test_forgot_password_nonexistent(client):
    resp = await client.post("/api/v1/auth/forgot-password", json={
        "email": "nobody@quickt.tg",
    })
    # Should still return 200 to prevent email enumeration
    assert resp.status_code == 200
