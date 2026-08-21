"""Development convenience script: seeds sample incidents, shelters, and users for local testing."""
import asyncio
import random

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.security import hash_password

SAMPLE_CITIES = [
    {"name": "San Francisco", "lon": -122.4194, "lat": 37.7749},
    {"name": "Manila", "lon": 120.9842, "lat": 14.5995},
    {"name": "Jakarta", "lon": 106.8456, "lat": -6.2088},
]


async def run():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]

    for city in SAMPLE_CITIES:
        await db["shelters"].insert_one(
            {
                "name": f"{city['name']} Community Shelter",
                "shelter_type": "combined",
                "location": {"type": "Point", "coordinates": [city["lon"], city["lat"]]},
                "address_text": f"Central District, {city['name']}",
                "status": "operational",
                "capacity_total": 200,
                "capacity_occupied": random.randint(20, 150),
                "accessibility_features": ["wheelchair_access"],
                "operating_hours": "24/7",
            }
        )
    print("Sample data seeded.")


if __name__ == "__main__":
    asyncio.run(run())
