import pytest


@pytest.mark.asyncio
async def test_create_shelter_requires_admin(app_client, auth_headers):
    resp = await app_client.post(
        "/api/v1/shelters",
        json={
            "name": "Test Shelter",
            "shelter_type": "emergency_shelter",
            "longitude": -122.4,
            "latitude": 37.7,
            "address_text": "123 Main St",
            "capacity_total": 100,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_nearby_shelters_is_public(app_client):
    resp = await app_client.get("/api/v1/shelters/nearby", params={"longitude": -122.4, "latitude": 37.7})
    assert resp.status_code == 200
