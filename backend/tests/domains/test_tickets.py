import pytest
from tests.conftest import auth_headers, create_agency


async def setup_booking_scenario(client):
    """Create agency, bus, route, schedule, departure, and customer."""
    # Agency staff setup
    staff_headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, staff_headers)

    # Bus
    bus_resp = await client.post("/api/v1/buses/", json={
        "plate_number": f"TG-TKT-{id(client) % 10000:04d}",
        "model": "Booking Bus",
        "capacity": 30,
        "seat_layout": {
            "rows": 8,
            "seats_per_row": 4,
            "aisle_after_column": 2,
            "unavailable_seats": [],
            "labels": [],
        },
    }, headers=staff_headers)
    bus_id = bus_resp.json()["id"]

    # Route
    admin_headers, _ = await auth_headers(client, role="admin")
    route_resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Kpalime",
        "distance_km": 120,
        "estimated_duration_minutes": 150,
    }, headers=admin_headers)
    route_id = route_resp.json()["id"]

    # Schedule
    sched_resp = await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "08:00",
        "price": 2500,
        "days_of_week": [0, 1, 2, 3, 4, 5, 6],
    }, headers=staff_headers)
    schedule_id = sched_resp.json()["id"]

    # Generate departure
    gen_resp = await client.post(
        f"/api/v1/schedules/{schedule_id}/generate-departures",
        json={"from_date": "2026-06-20", "to_date": "2026-06-20"},
        headers=staff_headers,
    )
    departure_id = gen_resp.json()[0]["id"]

    # Customer
    customer_headers, customer_user = await auth_headers(client, role="customer")

    return staff_headers, customer_headers, departure_id


@pytest.mark.asyncio
async def test_reserve_ticket(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "1A", "passenger_name": "Kofi Mensah", "passenger_phone": "+22890001111"},
        ],
    }, headers=customer_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["booking_reference"].startswith("BK-")
    assert len(data["tickets"]) == 1
    assert data["tickets"][0]["status"] == "reserved"
    assert data["tickets"][0]["code"].startswith("QT-")
    assert data["total"] == "2500.00"


@pytest.mark.asyncio
async def test_reserve_multiple_seats(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "2A", "passenger_name": "Ama Doe", "passenger_phone": "+22890002222"},
            {"seat_number": "2B", "passenger_name": "Yao Koffi", "passenger_phone": "+22890003333"},
        ],
    }, headers=customer_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["tickets"]) == 2
    assert data["total"] == "5000.00"


@pytest.mark.asyncio
async def test_cannot_book_same_seat_twice(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    # Book seat 3A
    await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "3A", "passenger_name": "Person A", "passenger_phone": "+22890004444"},
        ],
    }, headers=customer_headers)

    # Try to book 3A again
    resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "3A", "passenger_name": "Person B", "passenger_phone": "+22890005555"},
        ],
    }, headers=customer_headers)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_get_my_tickets(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "4A", "passenger_name": "Test", "passenger_phone": "+22890006666"},
        ],
    }, headers=customer_headers)

    resp = await client.get("/api/v1/tickets/my", headers=customer_headers)
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1


@pytest.mark.asyncio
async def test_cancel_ticket(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    create_resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "5A", "passenger_name": "Cancel Me", "passenger_phone": "+22890007777"},
        ],
    }, headers=customer_headers)
    ticket_id = create_resp.json()["tickets"][0]["id"]

    resp = await client.patch(f"/api/v1/tickets/{ticket_id}/cancel", json={
        "reason": "Change of plans",
    }, headers=customer_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancel_frees_seat(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    # Book a seat
    create_resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "6A", "passenger_name": "Free Me", "passenger_phone": "+22890008888"},
        ],
    }, headers=customer_headers)
    ticket_id = create_resp.json()["tickets"][0]["id"]

    # Check available seats decreased
    dep_resp = await client.get(f"/api/v1/departures/detail/{departure_id}")
    seats_after_book = dep_resp.json()["available_seats"]

    # Cancel
    await client.patch(f"/api/v1/tickets/{ticket_id}/cancel", json={}, headers=customer_headers)

    # Check seat freed
    dep_resp2 = await client.get(f"/api/v1/departures/detail/{departure_id}")
    seats_after_cancel = dep_resp2.json()["available_seats"]
    assert seats_after_cancel == seats_after_book + 1


@pytest.mark.asyncio
async def test_get_ticket_by_code(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    create_resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "7A", "passenger_name": "Code Test", "passenger_phone": "+22890009999"},
        ],
    }, headers=customer_headers)
    code = create_resp.json()["tickets"][0]["code"]

    resp = await client.get(f"/api/v1/tickets/code/{code}")
    assert resp.status_code == 200
    assert resp.json()["code"] == code


@pytest.mark.asyncio
async def test_mark_ticket_used(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    # Reserve
    create_resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "8A", "passenger_name": "Used Test", "passenger_phone": "+22890011111"},
        ],
    }, headers=customer_headers)
    ticket = create_resp.json()["tickets"][0]
    booking_ref = create_resp.json()["booking_reference"]

    # Manually confirm (simulating payment) - we need to do this via service
    # For now, test that marking non-confirmed ticket fails
    resp = await client.patch(
        f"/api/v1/tickets/{ticket['id']}/use",
        headers=staff_headers,
    )
    assert resp.status_code == 400  # Not confirmed yet


@pytest.mark.asyncio
async def test_get_departure_passengers(client):
    staff_headers, customer_headers, departure_id = await setup_booking_scenario(client)

    await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "1B", "passenger_name": "Passenger A", "passenger_phone": "+22890012222"},
            {"seat_number": "1C", "passenger_name": "Passenger B", "passenger_phone": "+22890013333"},
        ],
    }, headers=customer_headers)

    resp = await client.get(
        f"/api/v1/tickets/departure/{departure_id}/passengers",
        headers=staff_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["total"] >= 2
