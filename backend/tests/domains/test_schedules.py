import pytest
from tests.conftest import auth_headers, create_agency


async def setup_agency_with_bus_and_route(client):
    """Helper to create agency, bus, and route for schedule tests."""
    headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, headers)

    # Create bus
    bus_resp = await client.post("/api/v1/buses/", json={
        "plate_number": f"TG-SCH-{id(client) % 10000:04d}",
        "model": "Test Bus",
        "capacity": 30,
    }, headers=headers)
    bus_id = bus_resp.json()["id"]

    # Create route (need admin)
    admin_headers, _ = await auth_headers(client, role="admin")
    route_resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Kara",
        "distance_km": 420,
        "estimated_duration_minutes": 360,
    }, headers=admin_headers)
    route_id = route_resp.json()["id"]

    return headers, bus_id, route_id


@pytest.mark.asyncio
async def test_create_schedule(client):
    headers, bus_id, route_id = await setup_agency_with_bus_and_route(client)

    resp = await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "08:00",
        "price": 5000,
        "days_of_week": [0, 1, 2, 3, 4],
    }, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["price"] == "5000.00"
    assert data["days_of_week"] == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_list_schedules(client):
    headers, bus_id, route_id = await setup_agency_with_bus_and_route(client)

    await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "06:00",
        "price": 4000,
    }, headers=headers)
    await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "14:00",
        "price": 4500,
    }, headers=headers)

    resp = await client.get("/api/v1/schedules/", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


@pytest.mark.asyncio
async def test_generate_departures(client):
    headers, bus_id, route_id = await setup_agency_with_bus_and_route(client)

    sched_resp = await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "07:00",
        "price": 3500,
        "days_of_week": [0, 1, 2, 3, 4, 5, 6],
    }, headers=headers)
    schedule_id = sched_resp.json()["id"]

    resp = await client.post(f"/api/v1/schedules/{schedule_id}/generate-departures", json={
        "from_date": "2026-06-01",
        "to_date": "2026-06-07",
    }, headers=headers)
    assert resp.status_code == 200
    departures = resp.json()
    assert len(departures) == 7  # 7 days, all days of week


@pytest.mark.asyncio
async def test_generate_departures_no_duplicates(client):
    headers, bus_id, route_id = await setup_agency_with_bus_and_route(client)

    sched_resp = await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "09:00",
        "price": 4000,
        "days_of_week": [0, 1, 2, 3, 4, 5, 6],
    }, headers=headers)
    schedule_id = sched_resp.json()["id"]

    # Generate once
    resp1 = await client.post(f"/api/v1/schedules/{schedule_id}/generate-departures", json={
        "from_date": "2026-07-01",
        "to_date": "2026-07-03",
    }, headers=headers)
    assert len(resp1.json()) == 3

    # Generate again - should skip existing
    resp2 = await client.post(f"/api/v1/schedules/{schedule_id}/generate-departures", json={
        "from_date": "2026-07-01",
        "to_date": "2026-07-03",
    }, headers=headers)
    assert len(resp2.json()) == 0


@pytest.mark.asyncio
async def test_update_schedule(client):
    headers, bus_id, route_id = await setup_agency_with_bus_and_route(client)

    sched_resp = await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "10:00",
        "price": 3000,
    }, headers=headers)
    schedule_id = sched_resp.json()["id"]

    resp = await client.patch(f"/api/v1/schedules/{schedule_id}", json={
        "price": 3500,
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["price"] == "3500.00"
