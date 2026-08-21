from typing import Optional

from pydantic import BaseModel, Field

from app.models.alert import AlertSeverity


class AlertBroadcastRequest(BaseModel):
    title: str = Field(..., max_length=200)
    message: str = Field(..., max_length=2000)
    severity: AlertSeverity
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    radius_km: Optional[float] = Field(default=None, gt=0)
    expires_at: Optional[str] = None
