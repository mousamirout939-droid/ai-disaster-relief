"""Shared pytest fixtures: mocked or real MongoDB, test client, auth headers."""
import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security import create_access_token

USE_REAL_MONGO = os.getenv("USE_REAL_MONGO") == "1"
TEST_DB_NAME = "test_disaster_relief_db"


@pytest_asyncio.fixture
async def mock_db():
    if USE_REAL_MONGO:
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        client = AsyncIOMotorClient(mongo_uri)
        db = client[TEST_DB_NAME]
        await client.drop_database(TEST_DB_NAME)

        # $geoNear requires a 2dsphere index on the geo field. Real Mongo
        # enforces this; mongomock doesn't support $geoNear at all, which is
        # why this only matters when USE_REAL_MONGO=1.
        await db["incidents"].create_index([("location", "2dsphere")])

        yield db
        await client.drop_database(TEST_DB_NAME)
        client.close()
    else:
        client = AsyncMongoMockClient()
        yield client[TEST_DB_NAME]


@pytest_asyncio.fixture(autouse=True)
async def reset_redis_pool():
    """
    The Redis client in app.core.redis_client is a module-level singleton
    whose connection pool binds to whatever event loop is active when it's
    first used. If pytest-asyncio ever runs tests on separate event loops,
    stale connections from a previous loop cause 'RuntimeError: Event loop
    is closed'. Disconnecting here forces a fresh connection on the loop
    that is actually running for this test.
    """
    from app.core.redis_client import redis_client

    await redis_client.connection_pool.disconnect(inuse_connections=True)
    yield


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