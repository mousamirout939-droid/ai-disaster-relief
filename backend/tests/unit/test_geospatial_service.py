import pytest

from app.services.geospatial_service import GeospatialService


def test_haversine_distance_known_points():
    # San Francisco to Los Angeles is ~559 km
    distance = GeospatialService.haversine_distance_km(37.7749, -122.4194, 34.0522, -118.2437)
    assert 540 <= distance <= 580


def test_haversine_distance_same_point_is_zero():
    distance = GeospatialService.haversine_distance_km(10.0, 20.0, 10.0, 20.0)
    assert distance == pytest.approx(0.0, abs=1e-6)


def test_build_near_pipeline_structure():
    pipeline = GeospatialService.build_near_pipeline(-122.4, 37.7, 25.0)
    assert pipeline[0]["$geoNear"]["near"]["coordinates"] == [-122.4, 37.7]
    assert pipeline[0]["$geoNear"]["maxDistance"] == 25000
