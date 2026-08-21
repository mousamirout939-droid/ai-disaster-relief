import pytest


@pytest.mark.asyncio
async def test_register_and_login_flow(app_client):
    register_payload = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "SuperSecret123",
    }
    resp = await app_client.post("/api/v1/auth/register", json=register_payload)
    assert resp.status_code == 201

    login_resp = await app_client.post(
        "/api/v1/auth/login", json={"email": "testuser@example.com", "password": "SuperSecret123"}
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


@pytest.mark.asyncio
async def test_login_invalid_credentials_returns_401(app_client):
    resp = await app_client.post(
        "/api/v1/auth/login", json={"email": "nobody@example.com", "password": "wrong"}
    )
    assert resp.status_code == 401
