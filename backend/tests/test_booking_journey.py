"""
E2E test: Full booking journey.

Tests the complete happy path:
1. Register customer + agency staff + admin
2. Admin creates route
3. Agency creates bus, schedule, generates departures
4. Customer searches departures, reserves seats, pays, gets confirmed tickets
5. Agency views passenger list, marks ticket as used
"""

import pytest
from tests.conftest import auth_headers, create_agency, create_user, login


@pytest.mark.asyncio
async def test_full_booking_journey(client):
    # ---- 1. Register users ----
    admin_headers, _ = await auth_headers(client, role="admin")
    staff_headers, staff_user = await auth_headers(client, role="agency_staff")
    customer_headers, customer_user = await auth_headers(client, role="customer")

    # ---- 2. Agency staff creates agency ----
    agency = await create_agency(client, staff_headers, name="E2E Transport")

    # ---- 3. Admin creates route ----
    route_resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Kara",
        "distance_km": 420,
        "estimated_duration_minutes": 360,
    }, headers=admin_headers)
    assert route_resp.status_code == 201
    route = route_resp.json()

    # ---- 4. Agency creates bus ----
    bus_resp = await client.post("/api/v1/buses/", json={
        "plate_number": "TG-E2E-001",
        "model": "Mercedes Sprinter",
        "capacity": 30,
        "seat_layout": {
            "rows": 8,
            "seats_per_row": 4,
            "aisle_after_column": 2,
            "unavailable_seats": [],
            "labels": [],
        },
        "amenities": ["wifi", "ac"],
    }, headers=staff_headers)
    assert bus_resp.status_code == 201
    bus = bus_resp.json()

    # ---- 5. Agency creates schedule ----
    sched_resp = await client.post("/api/v1/schedules/", json={
        "route_id": route["id"],
        "bus_id": bus["id"],
        "departure_time": "07:30",
        "price": 5500,
        "days_of_week": [0, 1, 2, 3, 4, 5, 6],
    }, headers=staff_headers)
    assert sched_resp.status_code == 201
    schedule = sched_resp.json()

    # ---- 6. Agency generates departures ----
    gen_resp = await client.post(
        f"/api/v1/schedules/{schedule['id']}/generate-departures",
        json={"from_date": "2026-08-01", "to_date": "2026-08-07"},
        headers=staff_headers,
    )
    assert gen_resp.status_code == 200
    departures = gen_resp.json()
    assert len(departures) == 7

    # ---- 7. Customer searches departures ----
    search_resp = await client.get("/api/v1/departures/search", params={
        "origin": "Lome",
        "destination": "Kara",
        "date": "2026-08-01",
    })
    assert search_resp.status_code == 200
    results = search_resp.json()
    assert len(results) >= 1
    departure = results[0]
    assert departure["agency_name"] == "E2E Transport"
    assert departure["available_seats"] == 30

    # ---- 8. Customer views departure detail ----
    detail_resp = await client.get(f"/api/v1/departures/detail/{departure['id']}")
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert "seat_layout" in detail
    assert detail["amenities"] == ["wifi", "ac"]

    # ---- 9. Customer reserves seats ----
    reserve_resp = await client.post("/api/v1/tickets/", json={
        "departure_id": departure["id"],
        "seats": [
            {"seat_number": "1A", "passenger_name": "Kofi Mensah", "passenger_phone": "+22890001111"},
            {"seat_number": "1B", "passenger_name": "Ama Kofi", "passenger_phone": "+22890002222"},
        ],
    }, headers=customer_headers)
    assert reserve_resp.status_code == 201
    booking = reserve_resp.json()
    assert booking["booking_reference"].startswith("BK-")
    assert len(booking["tickets"]) == 2
    assert booking["total"] == "11000.00"  # 2 * 5500

    # Verify available seats decreased
    detail2 = await client.get(f"/api/v1/departures/detail/{departure['id']}")
    assert detail2.json()["available_seats"] == 28

    # ---- 10. Customer pays ----
    pay_resp = await client.post("/api/v1/payments/initiate", json={
        "booking_reference": booking["booking_reference"],
        "method": "flooz",
        "phone": "+22890001111",
    }, headers=customer_headers)
    assert pay_resp.status_code == 201
    payment = pay_resp.json()
    assert payment["status"] == "confirmed"  # sandbox auto-confirms
    assert payment["amount"] == "11000.00"

    # ---- 11. Verify tickets are confirmed with QR codes ----
    tickets_resp = await client.get("/api/v1/tickets/my", headers=customer_headers)
    tickets = tickets_resp.json()["items"]
    confirmed = [t for t in tickets if t["booking_reference"] == booking["booking_reference"]]
    assert len(confirmed) == 2
    for ticket in confirmed:
        assert ticket["status"] == "confirmed"
        assert ticket["qr_code_url"] is not None

    # ---- 12. Verify ticket by code (QR scan) ----
    code = confirmed[0]["code"]
    code_resp = await client.get(f"/api/v1/tickets/code/{code}")
    assert code_resp.status_code == 200
    assert code_resp.json()["status"] == "confirmed"

    # ---- 13. Agency views passenger list ----
    pass_resp = await client.get(
        f"/api/v1/tickets/departure/{departure['id']}/passengers",
        headers=staff_headers,
    )
    assert pass_resp.status_code == 200
    assert pass_resp.json()["total"] == 2

    # ---- 14. Agency marks ticket as used ----
    use_resp = await client.patch(
        f"/api/v1/tickets/{confirmed[0]['id']}/use",
        headers=staff_headers,
    )
    assert use_resp.status_code == 200
    assert use_resp.json()["status"] == "used"

    # ---- 15. Agency updates departure status ----
    status_resp = await client.patch(
        f"/api/v1/departures/{departure['id']}/status",
        json={"status": "boarding"},
        headers=staff_headers,
    )
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "boarding"

    # ---- 16. Customer views ticket detail ----
    ticket_detail = await client.get(
        f"/api/v1/tickets/{confirmed[0]['id']}",
        headers=customer_headers,
    )
    assert ticket_detail.status_code == 200
    td = ticket_detail.json()
    assert td["origin_city"] == "Lome"
    assert td["destination_city"] == "Kara"
    assert td["agency_name"] == "E2E Transport"

    # ---- 17. Customer creates trip plan ----
    trip_resp = await client.post("/api/v1/trips/", json={
        "route_id": route["id"],
        "planned_date": "2026-09-01",
        "notes": "Retour de Kara",
        "reminder_hours_before": 24,
    }, headers=customer_headers)
    assert trip_resp.status_code == 201

    # List trips
    trips = await client.get("/api/v1/trips/", headers=customer_headers)
    assert trips.status_code == 200
    assert len(trips.json()) >= 1

    # ---- 18. Payment history ----
    payments = await client.get("/api/v1/payments/my", headers=customer_headers)
    assert payments.status_code == 200
    assert len(payments.json()) >= 1
