from app.models.incident import IncidentDocument
from app.repositories.base_repository import BaseRepository
from app.services.geospatial_service import GeospatialService


class IncidentRepository(BaseRepository[IncidentDocument]):
    collection_name = "incidents"
    model_cls = IncidentDocument

    async def find_near(
        self, longitude: float, latitude: float, radius_km: float = 25.0, status: str | None = None
    ) -> list[IncidentDocument]:
        extra_match = {"status": status} if status else None
        docs = await GeospatialService.find_nearest(
            self.collection, longitude, latitude, radius_km, extra_match
        )
        return [IncidentDocument(**d) for d in docs]

    async def find_potential_duplicates(
        self, longitude: float, latitude: float, category: str, radius_km: float = 0.5
    ) -> list[IncidentDocument]:
        docs = await GeospatialService.find_nearest(
            self.collection, longitude, latitude, radius_km, {"category": category}, limit=10
        )
        return [IncidentDocument(**d) for d in docs]
