from app.models.shelter import ShelterDocument
from app.repositories.base_repository import BaseRepository
from app.services.geospatial_service import GeospatialService


class ShelterRepository(BaseRepository[ShelterDocument]):
    collection_name = "shelters"
    model_cls = ShelterDocument

    async def find_near(
        self, longitude: float, latitude: float, radius_km: float = 25.0, shelter_type: str | None = None
    ) -> list[ShelterDocument]:
        extra_match = {"status": "operational"}
        if shelter_type:
            extra_match["shelter_type"] = shelter_type
        docs = await GeospatialService.find_nearest(
            self.collection, longitude, latitude, radius_km, extra_match
        )
        return [ShelterDocument(**d) for d in docs]

    async def adjust_occupancy(self, shelter_id: str, delta: int) -> ShelterDocument | None:
        oid = self.to_object_id(shelter_id)
        if oid is None:
            return None
        await self.collection.update_one({"_id": oid}, {"$inc": {"capacity_occupied": delta}})
        doc = await self.collection.find_one({"_id": oid})
        return ShelterDocument(**doc) if doc else None
