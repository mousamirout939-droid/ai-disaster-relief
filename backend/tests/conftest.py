"""Shared pytest fixtures: mocked or real MongoDB, test client, auth headers."""
import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security import create_access_token

# Set USE_REAL_MONGO=1 in CI (or locally with Mongo running) to run tests
# against a real MongoDB instance instead of mongomock-motor. This is
# required for any test that uses aggregation features mongomock doesn't
# support, e.g. $geoNear.
USE_REAL_MONGO = os.getenv("USE_REAL_MONGO") == "1"
TEST_DB_NAME = "test_disaster_relief_db"


@pytest_asyncio.fixture
async def mock_db():
    if USE_REAL_MONGO:
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        client = AsyncIOMotorClient(mongo_uri)
        db = client[TEST_DB_NAME]
        # Ensure a clean slate for every test
        await client.drop_database(TEST_DB_NAME)
        yield db
        await client.drop_database(TEST_DB_NAME)
        client.close()
    else:
        client = AsyncMongoMockClient()
        yield client[TEST_DB_NAME]


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