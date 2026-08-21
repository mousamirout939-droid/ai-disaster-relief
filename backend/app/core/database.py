"""
Async MongoDB connection lifecycle management using Motor.
Handles connection pooling, index creation (including 2dsphere geospatial
indexes), and graceful shutdown. Wired into FastAPI's lifespan context.
"""
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, GEOSPHERE, TEXT
from pymongo.errors import PyMongoError

from app.core.config import settings

logger = logging.getLogger("app.database")


class MongoDatabase:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        logger.info("Connecting to MongoDB Atlas...")
        self.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
            uuidRepresentation="standard",
        )
        self.db = self.client[settings.MONGODB_DB_NAME]
        # Verify connectivity fast-fail on boot
        await self.client.admin.command("ping")
        await self._ensure_indexes()
        logger.info("MongoDB connection established: db=%s", settings.MONGODB_DB_NAME)

    async def disconnect(self) -> None:
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    async def _ensure_indexes(self) -> None:
        """Idempotent index creation, run on startup. Safe to re-run."""
        try:
            users = self.db["users"]
            await users.create_index([("email", ASCENDING)], unique=True)
            await users.create_index([("phone", ASCENDING)], unique=True, sparse=True)
            await users.create_index([("role", ASCENDING)])

            incidents = self.db["incidents"]
            await incidents.create_index([("location", GEOSPHERE)])
            await incidents.create_index([("status", ASCENDING), ("severity", DESCENDING)])
            await incidents.create_index([("reported_by", ASCENDING)])
            await incidents.create_index([("created_at", DESCENDING)])
            await incidents.create_index(
                [("description", TEXT), ("category", TEXT)], name="incident_text_search"
            )

            shelters = self.db["shelters"]
            await shelters.create_index([("location", GEOSPHERE)])
            await shelters.create_index([("status", ASCENDING)])

            inventory = self.db["inventory_logs"]
            await inventory.create_index([("shelter_id", ASCENDING), ("updated_at", DESCENDING)])

            alerts = self.db["alerts"]
            await alerts.create_index([("location", GEOSPHERE)])
            await alerts.create_index([("created_at", DESCENDING)])
            await alerts.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)

            audit_logs = self.db["audit_logs"]
            await audit_logs.create_index([("actor_id", ASCENDING), ("created_at", DESCENDING)])
            await audit_logs.create_index([("created_at", ASCENDING)], expireAfterSeconds=15552000)  # 180d

            aid_requests = self.db["aid_requests"]
            await aid_requests.create_index([("location", GEOSPHERE)])
            await aid_requests.create_index([("status", ASCENDING)])

            chat_sessions = self.db["chat_sessions"]
            await chat_sessions.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])

            logger.info("All MongoDB indexes verified/created (incl. 2dsphere geospatial).")
        except PyMongoError:
            logger.exception("Failed ensuring MongoDB indexes")
            raise

    def get_db(self) -> AsyncIOMotorDatabase:
        if self.db is None:
            raise RuntimeError("Database not initialized. Call connect() during app startup.")
        return self.db


mongo = MongoDatabase()


def get_database() -> AsyncIOMotorDatabase:
    """FastAPI dependency to inject the active database handle."""
    return mongo.get_db()
