"""Migration 002: Seed the initial platform administrator account from env vars."""
import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.security import hash_password


async def run():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]

    admin_email = os.environ.get("SEED_ADMIN_EMAIL", "admin@disaster-relief.platform")
    admin_password = os.environ.get("SEED_ADMIN_PASSWORD")
    if not admin_password:
        raise SystemExit("SEED_ADMIN_PASSWORD env var is required to seed the admin account.")

    existing = await db["users"].find_one({"email": admin_email})
    if existing:
        print("Admin already exists, skipping.")
        return

    await db["users"].insert_one(
        {
            "full_name": "Platform Administrator",
            "email": admin_email,
            "hashed_password": hash_password(admin_password),
            "role": "admin",
            "is_active": True,
            "is_suspended": False,
            "is_email_verified": True,
            "volunteer_verified": True,
            "preferred_language": "en",
            "notification_preferences": {"sms": True, "push": True, "email": True},
        }
    )
    print(f"Seeded admin account: {admin_email}")


if __name__ == "__main__":
    asyncio.run(run())
