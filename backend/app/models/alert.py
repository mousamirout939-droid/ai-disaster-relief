from enum import StrEnum
from datetime import datetime
from typing import Optional

from pydantic import Field

from app.models.base import GeoPoint, MongoBaseModel


class AlertSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertDocument(MongoBaseModel):
    title: str = Field(..., max_length=200)
    message: str = Field(..., max_length=2000)
    severity: AlertSeverity
    issued_by: str  # admin user id
    location: Optional[GeoPoint] = None  # None => platform-wide broadcast
    radius_km: Optional[float] = None
    affected_categories: list[str] = Field(default_factory=list)
    expires_at: Optional[datetime] = None
    channels: list[str] = Field(default_factory=lambda: ["push", "in_app"])
