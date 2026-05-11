import pytest
from tests.conftest import auth_headers, create_agency


@pytest.mark.asyncio
async def test_create_bus(client):
    headers, user = await auth_headers(client, role="agency_staff")
    agency = await create_agency(client, headers)

    resp = await client.post("/api/v1/buses/", json={
        "plate_number": "TG-1234-AB",
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
    }, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["plate_number"] == "TG-1234-AB"
    assert data["capacity"] == 30
    assert data["amenities"] == ["wifi", "ac"]


@pytest.mark.asyncio
async def test_create_bus_duplicate_plate(client):
    headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, headers)

    bus_data = {
        "plate_number": "TG-DUPE-01",
        "model": "Toyota Coaster",
        "capacity": 25,
    }
    resp1 = await client.post("/api/v1/buses/", json=bus_data, headers=headers)
    assert resp1.status_code == 201

    resp2 = await client.post("/api/v1/buses/", json=bus_data, headers=headers)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_list_buses(client):
    headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, headers)

    await client.post("/api/v1/buses/", json={
        "plate_number": "TG-LIST-01",
        "model": "Bus A",
        "capacity": 20,
    }, headers=headers)
    await client.post("/api/v1/buses/", json={
        "plate_number": "TG-LIST-02",
        "model": "Bus B",
        "capacity": 30,
    }, headers=headers)

    resp = await client.get("/api/v1/buses/", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2


@pytest.mark.asyncio
async def test_get_bus(client):
    headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, headers)

    create_resp = await client.post("/api/v1/buses/", json={
        "plate_number": "TG-GET-01",
        "model": "Bus Get",
        "capacity": 25,
    }, headers=headers)
    bus_id = create_resp.json()["id"]

    resp = await client.get(f"/api/v1/buses/{bus_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["plate_number"] == "TG-GET-01"


@pytest.mark.asyncio
async def test_update_bus(client):
    headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, headers)

    create_resp = await client.post("/api/v1/buses/", json={
        "plate_number": "TG-UPD-01",
        "model": "Old Model",
        "capacity": 20,
    }, headers=headers)
    bus_id = create_resp.json()["id"]

    resp = await client.patch(f"/api/v1/buses/{bus_id}", json={
        "model": "New Model",
        "capacity": 35,
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["model"] == "New Model"
    assert resp.json()["capacity"] == 35


@pytest.mark.asyncio
async def test_delete_bus(client):
    headers, _ = await auth_headers(client, role="agency_staff")
    await create_agency(client, headers)

    create_resp = await client.post("/api/v1/buses/", json={
        "plate_number": "TG-DEL-01",
        "model": "Delete Me",
        "capacity": 20,
    }, headers=headers)
    bus_id = create_resp.json()["id"]

    resp = await client.delete(f"/api/v1/buses/{bus_id}", headers=headers)
    assert resp.status_code == 204

    resp2 = await client.get(f"/api/v1/buses/{bus_id}", headers=headers)
    assert resp2.status_code == 404


@pytest.mark.asyncio
async def test_customer_cannot_manage_buses(client):
    headers, _ = await auth_headers(client, role="customer")
    resp = await client.post("/api/v1/buses/", json={
        "plate_number": "TG-NO-01",
        "model": "Nope",
        "capacity": 20,
    }, headers=headers)
    assert resp.status_code == 403
