import pytest
from tests.conftest import auth_headers, create_agency


async def setup_booking_with_tickets(client):
    """Create a complete booking: agency + bus + route + schedule + departure + tickets."""
    staff_headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, staff_headers)

    bus_resp = await client.post("/api/v1/buses/", json={
        "plate_number": f"TG-PAY-{id(client) % 10000:04d}",
        "model": "Payment Bus",
        "capacity": 30,
    }, headers=staff_headers)
    bus_id = bus_resp.json()["id"]

    admin_headers, _ = await auth_headers(client, role="admin")
    route_resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Dapaong",
        "distance_km": 620,
        "estimated_duration_minutes": 540,
    }, headers=admin_headers)
    route_id = route_resp.json()["id"]

    sched_resp = await client.post("/api/v1/schedules/", json={
        "route_id": route_id,
        "bus_id": bus_id,
        "departure_time": "06:00",
        "price": 8000,
        "days_of_week": [0, 1, 2, 3, 4, 5, 6],
    }, headers=staff_headers)
    schedule_id = sched_resp.json()["id"]

    gen_resp = await client.post(
        f"/api/v1/schedules/{schedule_id}/generate-departures",
        json={"from_date": "2026-07-01", "to_date": "2026-07-01"},
        headers=staff_headers,
    )
    departure_id = gen_resp.json()[0]["id"]

    customer_headers, _ = await auth_headers(client, role="customer")
    ticket_resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure_id,
        "seats": [
            {"seat_number": "1A", "passenger_name": "Kofi Test", "passenger_phone": "+22890001111"},
            {"seat_number": "1B", "passenger_name": "Ama Test", "passenger_phone": "+22890002222"},
        ],
    }, headers=customer_headers)
    booking_ref = ticket_resp.json()["booking_reference"]

    return staff_headers, customer_headers, booking_ref, departure_id


@pytest.mark.asyncio
async def test_initiate_payment(client):
    staff_headers, customer_headers, booking_ref, _ = await setup_booking_with_tickets(client)

    resp = await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking_ref,
        "method": "flooz",
        "phone": "+22890001111",
    }, headers=customer_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["booking_reference"] == booking_ref
    assert data["amount"] == "16000.00"  # 2 seats * 8000
    assert data["method"] == "flooz"
    # In sandbox mode, payment is auto-confirmed
    assert data["status"] == "confirmed"


@pytest.mark.asyncio
async def test_payment_confirms_tickets(client):
    staff_headers, customer_headers, booking_ref, _ = await setup_booking_with_tickets(client)

    # Pay
    await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking_ref,
        "method": "t_money",
        "phone": "+22890003333",
    }, headers=customer_headers)

    # Check tickets are confirmed
    tickets_resp = await client.get("/api/v1/tickets/my", headers=customer_headers)
    tickets = tickets_resp.json()["items"]
    for ticket in tickets:
        if ticket["booking_reference"] == booking_ref:
            assert ticket["status"] == "confirmed"
            assert ticket["qr_code_url"] is not None


@pytest.mark.asyncio
async def test_payment_status(client):
    _, customer_headers, booking_ref, _ = await setup_booking_with_tickets(client)

    pay_resp = await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking_ref,
        "method": "flooz",
        "phone": "+22890004444",
    }, headers=customer_headers)
    payment_id = pay_resp.json()["id"]

    resp = await client.get(f"/api/v1/payments/{payment_id}/status")
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


@pytest.mark.asyncio
async def test_duplicate_payment_rejected(client):
    _, customer_headers, booking_ref, _ = await setup_booking_with_tickets(client)

    # First payment
    resp1 = await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking_ref,
        "method": "flooz",
        "phone": "+22890005555",
    }, headers=customer_headers)
    assert resp1.status_code == 201

    # Second payment for same booking should fail (tickets already confirmed)
    resp2 = await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking_ref,
        "method": "flooz",
        "phone": "+22890005555",
    }, headers=customer_headers)
    assert resp2.status_code == 404  # No reserved tickets left


@pytest.mark.asyncio
async def test_my_payments(client):
    _, customer_headers, booking_ref, _ = await setup_booking_with_tickets(client)

    await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking_ref,
        "method": "flooz",
        "phone": "+22890006666",
    }, headers=customer_headers)

    resp = await client.get("/api/v1/payments/my", headers=customer_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_invalid_payment_method(client):
    _, customer_headers, booking_ref, _ = await setup_booking_with_tickets(client)

    resp = await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking_ref,
        "method": "bitcoin",
        "phone": "+22890007777",
    }, headers=customer_headers)
    assert resp.status_code == 400
