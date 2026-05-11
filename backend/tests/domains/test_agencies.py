from tests.conftest import auth_headers, create_agency


async def test_create_agency(client):
    headers, _ = await auth_headers(client)
    resp = await client.post("/api/v1/agencies/", json={
        "name": "Test Agency",
        "description": "A test agency",
        "phone": "+22890999999",
        "email": "test@agency.tg",
        "address": "123 Agency St",
        "city": "Lome",
        "region": "Maritime",
    }, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Agency"
    assert data["slug"] == "test-agency"
    assert data["status"] == "pending"

    # Verify user is now agency_staff
    me_resp = await client.get("/api/v1/auth/me", headers=headers)
    me_data = me_resp.json()
    assert me_data["role"] == "agency_staff"
    assert me_data["agency_id"] == data["id"]


async def test_list_agencies_public(client):
    # Public listing only shows approved agencies
    headers, _ = await auth_headers(client)
    await create_agency(client, headers)

    resp = await client.get("/api/v1/agencies/")
    assert resp.status_code == 200
    data = resp.json()
    # Newly created agencies are pending, so shouldn't appear in public list
    assert data["total"] == 0


async def test_get_agency(client):
    headers, _ = await auth_headers(client)
    agency = await create_agency(client, headers)
    resp = await client.get(f"/api/v1/agencies/{agency['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == agency["name"]


async def test_approve_agency(client):
    # Create agency
    user_headers, _ = await auth_headers(client)
    agency = await create_agency(client, user_headers)

    # Approve as admin
    admin_headers, _ = await auth_headers(client, role="admin")
    resp = await client.patch(
        f"/api/v1/agencies/{agency['id']}/approve",
        headers=admin_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "approved"
    assert resp.json()["approved_at"] is not None


async def test_suspend_agency(client):
    user_headers, _ = await auth_headers(client)
    agency = await create_agency(client, user_headers)

    admin_headers, _ = await auth_headers(client, role="admin")
    # Approve first
    await client.patch(f"/api/v1/agencies/{agency['id']}/approve", headers=admin_headers)

    # Then suspend
    resp = await client.patch(
        f"/api/v1/agencies/{agency['id']}/suspend",
        headers=admin_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "suspended"


async def test_update_agency(client):
    headers, _ = await auth_headers(client)
    agency = await create_agency(client, headers)
    # Re-login to get fresh headers with agency_staff role
    from tests.conftest import login
    headers = await login(client, _["email"])

    resp = await client.patch(f"/api/v1/agencies/{agency['id']}", json={
        "description": "Updated description",
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated description"


async def test_non_admin_cannot_approve(client):
    user_headers, _ = await auth_headers(client)
    agency = await create_agency(client, user_headers)

    other_headers, _ = await auth_headers(client)
    resp = await client.patch(
        f"/api/v1/agencies/{agency['id']}/approve",
        headers=other_headers,
    )
    assert resp.status_code == 403
