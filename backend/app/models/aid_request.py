from enum import StrEnum

from pydantic import Field

from app.models.base import GeoPoint, MongoBaseModel


class AidRequestStatus(StrEnum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    DISPATCHED = "dispatched"
    FULFILLED = "fulfilled"
    DENIED = "denied"


class AidRequestDocument(MongoBaseModel):
    requested_by: str
    location: GeoPoint
    needs: list[str] = Field(default_factory=list)  # e.g. ["food", "medical", "rescue"]
    household_size: int = Field(default=1, ge=1)
    has_vulnerable_members: bool = False  # elderly, disabled, infants
    description: str = Field(..., max_length=1500)
    status: AidRequestStatus = AidRequestStatus.SUBMITTED
    assigned_to: str | None = None
    linked_incident_id: str | None = None
