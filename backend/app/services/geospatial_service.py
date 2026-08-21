"""
Reusable geospatial query helpers built on MongoDB's 2dsphere indexes.
Centralizing this logic avoids duplicating aggregation pipelines across
incident, shelter, and alert repositories.
"""
from motor.motor_asyncio import AsyncIOMotorCollection


class GeospatialService:
    EARTH_RADIUS_METERS = 6_378_137

    @staticmethod
    def build_near_pipeline(
        longitude: float,
        latitude: float,
        max_distance_km: float,
        extra_match: dict | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """
        Builds a $geoNear aggregation stage — must be the FIRST stage in the
        pipeline per MongoDB requirements. Returns documents sorted nearest-first
        with a computed `distance_meters` field.
        """
        geo_near_stage = {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": [longitude, latitude]},
                "distanceField": "distance_meters",
                "maxDistance": max_distance_km * 1000,
                "spherical": True,
                "query": extra_match or {},
            }
        }
        return [geo_near_stage, {"$limit": limit}]

    @staticmethod
    def build_within_radius_filter(longitude: float, latitude: float, radius_km: float) -> dict:
        """Simple $geoWithin $centerSphere filter (no distance sort needed)."""
        radius_radians = radius_km / (GeospatialService.EARTH_RADIUS_METERS / 1000)
        return {
            "location": {
                "$geoWithin": {"$centerSphere": [[longitude, latitude], radius_radians]}
            }
        }

    @staticmethod
    async def find_nearest(
        collection: AsyncIOMotorCollection,
        longitude: float,
        latitude: float,
        max_distance_km: float = 25.0,
        extra_match: dict | None = None,
        limit: int = 100,
    ) -> list[dict]:
        pipeline = GeospatialService.build_near_pipeline(
            longitude, latitude, max_distance_km, extra_match, limit
        )
        return await collection.aggregate(pipeline).to_list(length=limit)

    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Fallback pure-python distance calc (used for client-side / test validation)."""
        from math import atan2, cos, radians, sin, sqrt

        r = 6371.0  # km
        phi1, phi2 = radians(lat1), radians(lat2)
        d_phi = radians(lat2 - lat1)
        d_lambda = radians(lon2 - lon1)
        a = sin(d_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(d_lambda / 2) ** 2
        return 2 * r * atan2(sqrt(a), sqrt(1 - a))
