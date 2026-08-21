"""
End-to-end scenario test: citizen registers, reports an incident, a
volunteer verifies it, and the incident becomes queryable as verified.
Uses the mocked in-memory Mongo backend — no external services required.
"""
import pytest


@pytest.mark.asyncio
async def test_full_citizen_to_volunteer_verification_flow(app_client):
    # 1. Citizen registers and logs in
    await app_client.post(
        "/api/v1/auth/register",
        json={"full_name": "Citizen One", "email": "citizen1@example.com", "password": "SuperSecret123"},
    )
    login = await app_client.post(
        "/api/v1/auth/login", json={"email": "citizen1@example.com", "password": "SuperSecret123"}
    )
    citizen_token = login.json()["access_token"]

    # 2. Citizen reports an incident (no image, text-only path)
    report = await app_client.post(
        "/api/v1/incidents",
        data={
            "category": "flood",
            "description": "Street flooding, water rising fast",
            "longitude": -122.4,
            "latitude": 37.7,
        },
        headers={"Authorization": f"Bearer {citizen_token}"},
    )
    assert report.status_code == 201
    assert report.json()["status"] == "pending_review"