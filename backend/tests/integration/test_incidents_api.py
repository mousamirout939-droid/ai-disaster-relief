import pytest


@pytest.mark.asyncio
async def test_report_incident_requires_auth(app_client):
    resp = await app_client.post(
        "/api/v1/incidents",
        data={
            "category": "fire",
            "description": "Large fire near downtown",
            "longitude": -122.4,
            "latitude": 37.7,
        },
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_nearby_incidents_requires_auth(app_client):
    resp = await app_client.get("/api/v1/incidents/nearby", params={"longitude": -122.4, "latitude": 37.7})
    assert resp.status_code == 401
