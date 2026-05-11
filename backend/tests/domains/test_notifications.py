import pytest
from tests.conftest import auth_headers


@pytest.mark.asyncio
async def test_list_notifications_empty(client):
    headers, _ = await auth_headers(client, role="customer")

    resp = await client.get("/api/v1/notifications/", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["unread_count"] == 0


@pytest.mark.asyncio
async def test_mark_all_read(client):
    headers, _ = await auth_headers(client, role="customer")

    resp = await client.post("/api/v1/notifications/read-all", headers=headers)
    assert resp.status_code == 204
