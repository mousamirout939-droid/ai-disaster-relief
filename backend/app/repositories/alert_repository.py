from app.models.alert import AlertDocument
from app.repositories.base_repository import BaseRepository
from app.services.geospatial_service import GeospatialService


class AlertRepository(BaseRepository[AlertDocument]):
    collection_name = "alerts"
    model_cls = AlertDocument

    async def find_active_near(self, longitude: float, latitude: float, radius_km: float = 50.0):
        pipeline = GeospatialService.build_near_pipeline(longitude, latitude, radius_km, limit=50)
        docs = await self.collection.aggregate(pipeline).to_list(length=50)
        return [AlertDocument(**d) for d in docs]

    async def find_platform_wide(self) -> list[AlertDocument]:
        cursor = self.collection.find({"location": None}).sort("created_at", -1).limit(50)
        docs = await cursor.to_list(length=50)
        return [AlertDocument(**d) for d in docs]
