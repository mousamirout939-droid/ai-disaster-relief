"""Shared pytest fixtures: mocked MongoDB (mongomock-motor), test client, auth headers."""
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.core.security import create_access_token


@pytest_asyncio.fixture
async def mock_db():
    client = AsyncMongoMockClient()
    return client["test_disaster_relief_db"]


@pytest_asyncio.fixture
async def app_client(mock_db, monkeypatch):
    from app.core.database import mongo
    from app.main import app

    mongo.db = mock_db
    mongo.client = mock_db.client

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def citizen_token():
    return create_access_token("507f1f77bcf86cd799439011", "citizen")


@pytest.fixture
def volunteer_token():
    return create_access_token("507f1f77bcf86cd799439012", "volunteer")


@pytest.fixture
def admin_token():
    return create_access_token("507f1f77bcf86cd799439013", "admin")


@pytest.fixture
def auth_headers(citizen_token):
    return {"Authorization": f"Bearer {citizen_token}"}
