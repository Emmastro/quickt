import pytest
from tests.conftest import auth_headers


async def create_route(client):
    admin_headers, _ = await auth_headers(client, role="admin")
    resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Kpalime",
        "distance_km": 120,
        "estimated_duration_minutes": 150,
    }, headers=admin_headers)
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_trip(client):
    headers, _ = await auth_headers(client, role="customer")
    route_id = await create_route(client)

    resp = await client.post("/api/v1/trips/", json={
        "route_id": route_id,
        "planned_date": "2026-07-15",
        "notes": "Voyage famille",
        "reminder_hours_before": 12,
    }, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["planned_date"] == "2026-07-15"
    assert data["reminder_hours_before"] == 12


@pytest.mark.asyncio
async def test_list_trips(client):
    headers, _ = await auth_headers(client, role="customer")
    route_id = await create_route(client)

    await client.post("/api/v1/trips/", json={
        "route_id": route_id,
        "planned_date": "2026-07-20",
    }, headers=headers)

    resp = await client.get("/api/v1/trips/", headers=headers)
    assert resp.status_code == 200
    trips = resp.json()
    assert len(trips) >= 1
    assert trips[0]["origin_city"] == "Lome"


@pytest.mark.asyncio
async def test_update_trip(client):
    headers, _ = await auth_headers(client, role="customer")
    route_id = await create_route(client)

    create_resp = await client.post("/api/v1/trips/", json={
        "route_id": route_id,
        "planned_date": "2026-08-01",
    }, headers=headers)
    trip_id = create_resp.json()["id"]

    resp = await client.patch(f"/api/v1/trips/{trip_id}", json={
        "notes": "Updated notes",
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["notes"] == "Updated notes"


@pytest.mark.asyncio
async def test_delete_trip(client):
    headers, _ = await auth_headers(client, role="customer")
    route_id = await create_route(client)

    create_resp = await client.post("/api/v1/trips/", json={
        "route_id": route_id,
        "planned_date": "2026-08-10",
    }, headers=headers)
    trip_id = create_resp.json()["id"]

    resp = await client.delete(f"/api/v1/trips/{trip_id}", headers=headers)
    assert resp.status_code == 204
