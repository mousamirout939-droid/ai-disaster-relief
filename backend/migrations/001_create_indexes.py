"""
Migration 001: Bootstrap all collection indexes, including 2dsphere geospatial
indexes. Idempotent — safe to re-run. In production this is also invoked
automatically on app startup via app.core.database.MongoDatabase._ensure_indexes,
but is kept here as an explicit, auditable migration step for CI/CD pipelines.
"""
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


async def run():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    from app.core.database import MongoDatabase

    mongo = MongoDatabase()
    mongo.client = client
    mongo.db = db
    await mongo._ensure_indexes()
    print("Migration 001 complete: indexes created.")


if __name__ == "__main__":
    asyncio.run(run())
