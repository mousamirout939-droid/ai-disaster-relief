from enum import StrEnum
from typing import Optional

from pydantic import Field

from app.models.base import GeoPoint, MongoBaseModel


class ShelterStatus(StrEnum):
    OPERATIONAL = "operational"
    AT_CAPACITY = "at_capacity"
    CLOSED = "closed"
    STANDBY = "standby"


class ShelterType(StrEnum):
    EMERGENCY_SHELTER = "emergency_shelter"
    FOOD_DISTRIBUTION = "food_distribution"
    MEDICAL_STATION = "medical_station"
    COMBINED = "combined"


class ShelterDocument(MongoBaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    shelter_type: ShelterType
    location: GeoPoint
    address_text: str
    status: ShelterStatus = ShelterStatus.OPERATIONAL
    capacity_total: int = Field(ge=0)
    capacity_occupied: int = Field(default=0, ge=0)
    managed_by: Optional[str] = None  # volunteer/org user id
    contact_phone: Optional[str] = None
    accessibility_features: list[str] = Field(default_factory=list)
    operating_hours: str = "24/7"

    @property
    def capacity_available(self) -> int:
        return max(self.capacity_total - self.capacity_occupied, 0)
