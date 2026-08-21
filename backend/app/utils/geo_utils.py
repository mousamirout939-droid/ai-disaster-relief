"""Standalone geo utility functions not tied to MongoDB (used in schemas/validators/tests)."""

def is_valid_longitude(lon: float) -> bool:
    return -180.0 <= lon <= 180.0


def is_valid_latitude(lat: float) -> bool:
    return -90.0 <= lat <= 90.0


def bounding_box(lon: float, lat: float, radius_km: float) -> dict:
    """Rough bounding box for quick pre-filtering before precise geo queries."""
    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * max(0.01, abs(__import__("math").cos(__import__("math").radians(lat)))))
    return {
        "min_lat": lat - lat_delta,
        "max_lat": lat + lat_delta,
        "min_lon": lon - lon_delta,
        "max_lon": lon + lon_delta,
    }
