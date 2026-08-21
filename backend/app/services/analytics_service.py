"""Platform-wide analytics aggregations for the admin dashboard."""
from motor.motor_asyncio import AsyncIOMotorDatabase


class AnalyticsService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_incident_summary(self) -> dict:
        pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
        results = await self.db["incidents"].aggregate(pipeline).to_list(length=20)
        return {r["_id"]: r["count"] for r in results}

    async def get_severity_breakdown(self) -> dict:
        pipeline = [{"$group": {"_id": "$severity", "count": {"$sum": 1}}}]
        results = await self.db["incidents"].aggregate(pipeline).to_list(length=20)
        return {r["_id"]: r["count"] for r in results}

    async def get_shelter_capacity_overview(self) -> dict:
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_capacity": {"$sum": "$capacity_total"},
                    "total_occupied": {"$sum": "$capacity_occupied"},
                    "shelter_count": {"$sum": 1},
                }
            }
        ]
        results = await self.db["shelters"].aggregate(pipeline).to_list(length=1)
        return results[0] if results else {"total_capacity": 0, "total_occupied": 0, "shelter_count": 0}

    async def get_incidents_over_time(self, days: int = 30) -> list[dict]:
        pipeline = [
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
            {"$limit": days},
        ]
        return await self.db["incidents"].aggregate(pipeline).to_list(length=days)
