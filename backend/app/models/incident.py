from enum import StrEnum
from typing import Optional

from pydantic import Field

from app.models.base import GeoPoint, MongoBaseModel


class IncidentCategory(StrEnum):
    FLOOD = "flood"
    FIRE = "fire"
    EARTHQUAKE = "earthquake"
    HURRICANE = "hurricane"
    LANDSLIDE = "landslide"
    BUILDING_COLLAPSE = "building_collapse"
    MEDICAL_EMERGENCY = "medical_emergency"
    OTHER = "other"


class IncidentSeverity(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"


class AISeverityAnalysis(MongoBaseModel):
    """Embedded sub-document: result of YOLOv8 severity inference on an uploaded image."""

    model_version: str
    predicted_severity: IncidentSeverity
    confidence: float = Field(ge=0.0, le=1.0)
    detected_objects: list[dict] = Field(default_factory=list)  # [{label, confidence, bbox}]
    inference_ms: float


class IncidentDocument(MongoBaseModel):
    reported_by: str  # user id
    category: IncidentCategory
    description: str = Field(..., min_length=5, max_length=2000)
    location: GeoPoint
    address_text: Optional[str] = None
    image_urls: list[str] = Field(default_factory=list)
    ai_analysis: Optional[AISeverityAnalysis] = None
    severity: IncidentSeverity = IncidentSeverity.MODERATE
    status: IncidentStatus = IncidentStatus.PENDING_REVIEW
    verified_by: Optional[str] = None  # volunteer/admin user id
    verified_at: Optional[str] = None
    duplicate_of: Optional[str] = None
    people_affected_estimate: Optional[int] = None
    upvote_count: int = 0  # community corroboration signal
