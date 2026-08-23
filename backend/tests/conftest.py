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
    app.core.redis_client is a module-level singleton whose connection pool
    binds to whatever event loop is running when it's first used. With
    pytest-asyncio's default function-scoped loops, each test gets a fresh
    loop, so connections from a previous test reference an already-closed
    loop. Gracefully closing them (pool.disconnect()) fails because it tries
    to touch that dead loop. Since the old loop and its sockets are already
    gone, we just drop the stale references directly instead of trying to
    close them - the pool then transparently opens fresh connections on the
    current test's loop on next use.
    """
    from app.core.redis_client import redis_client

    pool = redis_client.connection_pool
    pool._available_connections.clear()
    pool._in_use_connections.clear()
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