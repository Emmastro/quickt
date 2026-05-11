import pytest
from tests.conftest import auth_headers, create_agency


async def setup_departure(client):
    """Create agency, bus, route, schedule, and generate a departure."""
    headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, headers)

    # Create bus
    bus_resp = await client.post("/api/v1/buses/", json={
        "plate_number": f"TG-DEP-{id(client) % 10000:04d}",
        "model": "Test Bus",
        "capacity": 30,
        "seat_layout": {
            "rows": 8,
            "seats_per_row": 4,
            "aisle_after_column": 2,
            "unavailable_seats": [],
            "labels": [],
        },
    }, headers=headers)
    bus_id = bus_resp.json()["id"]

    # Create route
    admin_headers, _ = await auth_headers(client, role="admin")
    route_resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Sokode",
        "distance_km": 340,
        "estimated_duration_minutes": 300,
    }, headers=admin_headers)
    route_id = route_resp.json()["id"]

    # Create schedule
    sched_resp = await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "07:00",
        "price": 4500,
        "days_of_week": [0, 1, 2, 3, 4, 5, 6],
    }, headers=headers)
    schedule_id = sched_resp.json()["id"]

    # Generate departures
    gen_resp = await client.post(
        f"/api/v1/schedules/{schedule_id}/generate-departures",
        json={"from_date": "2026-06-15", "to_date": "2026-06-15"},
        headers=headers,
    )
    departure_id = gen_resp.json()[0]["id"]

    return headers, departure_id


@pytest.mark.asyncio
async def test_search_departures(client):
    headers, departure_id = await setup_departure(client)

    resp = await client.get("/api/v1/departures/search", params={
        "origin": "Lome",
        "destination": "Sokode",
        "date": "2026-06-15",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert data[0]["origin_city"] == "Lome"
    assert data[0]["destination_city"] == "Sokode"
    assert data[0]["available_seats"] == 30


@pytest.mark.asyncio
async def test_search_no_results(client):
    resp = await client.get("/api/v1/departures/search", params={
        "origin": "Nowhere",
        "destination": "Nope",
        "date": "2026-06-15",
    })
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_get_departure_detail(client):
    headers, departure_id = await setup_departure(client)

    resp = await client.get(f"/api/v1/departures/detail/{departure_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["origin_city"] == "Lome"
    assert data["destination_city"] == "Sokode"
    assert "seat_layout" in data
    assert data["total_seats"] == 30


@pytest.mark.asyncio
async def test_list_agency_departures(client):
    headers, departure_id = await setup_departure(client)

    resp = await client.get("/api/v1/departures/", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1


@pytest.mark.asyncio
async def test_update_departure_status(client):
    headers, departure_id = await setup_departure(client)

    # scheduled -> boarding
    resp = await client.patch(
        f"/api/v1/departures/{departure_id}/status",
        json={"status": "boarding"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "boarding"

    # boarding -> departed
    resp2 = await client.patch(
        f"/api/v1/departures/{departure_id}/status",
        json={"status": "departed"},
        headers=headers,
    )
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "departed"


@pytest.mark.asyncio
async def test_invalid_status_transition(client):
    headers, departure_id = await setup_departure(client)

    # scheduled -> completed is not allowed
    resp = await client.patch(
        f"/api/v1/departures/{departure_id}/status",
        json={"status": "completed"},
        headers=headers,
    )
    assert resp.status_code == 400
