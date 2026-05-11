from tests.conftest import auth_headers


async def test_create_route(client):
    admin_headers, _ = await auth_headers(client, role="admin")
    resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Kpalime",
        "distance_km": 120,
        "estimated_duration_minutes": 150,
    }, headers=admin_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["origin_city"] == "Lome"
    assert data["destination_city"] == "Kpalime"
    assert data["duration_display"] == "2h 30min"


async def test_create_route_duplicate(client):
    admin_headers, _ = await auth_headers(client, role="admin")
    await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Sokode",
        "estimated_duration_minutes": 300,
    }, headers=admin_headers)
    resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Sokode",
        "estimated_duration_minutes": 300,
    }, headers=admin_headers)
    assert resp.status_code == 409


async def test_list_routes(client):
    admin_headers, _ = await auth_headers(client, role="admin")
    await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Kara",
        "distance_km": 420,
        "estimated_duration_minutes": 360,
    }, headers=admin_headers)
    await client.post("/api/v1/routes/", json={
        "origin_city": "Sokode",
        "destination_city": "Kara",
        "distance_km": 180,
        "estimated_duration_minutes": 150,
    }, headers=admin_headers)

    resp = await client.get("/api/v1/routes/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2


async def test_search_routes_by_origin(client):
    admin_headers, _ = await auth_headers(client, role="admin")
    await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Dapaong",
        "estimated_duration_minutes": 540,
    }, headers=admin_headers)
    await client.post("/api/v1/routes/", json={
        "origin_city": "Kara",
        "destination_city": "Dapaong",
        "estimated_duration_minutes": 180,
    }, headers=admin_headers)

    resp = await client.get("/api/v1/routes/?origin=Lome")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["origin_city"] == "Lome"


async def test_get_route(client):
    admin_headers, _ = await auth_headers(client, role="admin")
    create_resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Tsevie",
        "distance_km": 35,
        "estimated_duration_minutes": 45,
    }, headers=admin_headers)
    route_id = create_resp.json()["id"]

    resp = await client.get(f"/api/v1/routes/{route_id}")
    assert resp.status_code == 200
    assert resp.json()["destination_city"] == "Tsevie"


async def test_get_popular_routes(client):
    admin_headers, _ = await auth_headers(client, role="admin")
    await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Aneho",
        "estimated_duration_minutes": 60,
    }, headers=admin_headers)

    resp = await client.get("/api/v1/routes/popular")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_non_admin_cannot_create_route(client):
    headers, _ = await auth_headers(client)
    resp = await client.post("/api/v1/routes/", json={
        "origin_city": "Lome",
        "destination_city": "Kpalime",
        "estimated_duration_minutes": 150,
    }, headers=headers)
    assert resp.status_code == 403
