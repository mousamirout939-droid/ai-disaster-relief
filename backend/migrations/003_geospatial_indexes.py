"""
Migration 003: Verifies 2dsphere indexes exist on all location-bearing
collections and reports index build status. Useful as a standalone CI check
independent of full index bootstrap in 001.
"""
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

GEO_COLLECTIONS = ["incidents", "shelters", "alerts", "aid_requests"]


async def run():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    for coll_name in GEO_COLLECTIONS:
        indexes = await db[coll_name].index_information()
        has_geo = any(
            any(k[1] == "2dsphere" for k in idx.get("key", [])) for idx in indexes.values()
        )
        status = "OK" if has_geo else "MISSING"
        print(f"[{status}] {coll_name}.location 2dsphere index")


if __name__ == "__main__":
    asyncio.run(run())
