from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.base import GeoPoint, PyObjectId
from app.models.incident import AISeverityAnalysis, IncidentCategory, IncidentSeverity, IncidentStatus


class IncidentCreateRequest(BaseModel):
    category: IncidentCategory
    description: str = Field(..., min_length=5, max_length=2000)
    longitude: float
    latitude: float
    address_text: Optional[str] = None
    people_affected_estimate: Optional[int] = None


class IncidentResponse(BaseModel):
    id: PyObjectId
    reported_by: str
    category: IncidentCategory
    description: str
    location: GeoPoint
    address_text: Optional[str]
    image_urls: list[str]
    ai_analysis: Optional[AISeverityAnalysis]
    severity: IncidentSeverity
    status: IncidentStatus
    verified_by: Optional[str]
    created_at: datetime


class IncidentVerifyRequest(BaseModel):
    approve: bool
    notes: Optional[str] = None
