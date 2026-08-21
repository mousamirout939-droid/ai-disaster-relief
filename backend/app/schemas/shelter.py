from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.base import GeoPoint, PyObjectId
from app.models.shelter import ShelterStatus, ShelterType


class ShelterCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    shelter_type: ShelterType
    longitude: float
    latitude: float
    address_text: str
    capacity_total: int = Field(ge=0)
    contact_phone: Optional[str] = None
    accessibility_features: list[str] = Field(default_factory=list)


class ShelterResponse(BaseModel):
    id: PyObjectId
    name: str
    shelter_type: ShelterType
    location: GeoPoint
    address_text: str
    status: ShelterStatus
    capacity_total: int
    capacity_occupied: int
    capacity_available: int
    contact_phone: Optional[str]
    created_at: datetime


class ShelterUpdateRequest(BaseModel):
    status: Optional[ShelterStatus] = None
    capacity_occupied: Optional[int] = None
    contact_phone: Optional[str] = None
