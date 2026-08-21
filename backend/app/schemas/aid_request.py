from pydantic import BaseModel, Field

from app.models.aid_request import AidRequestStatus


class AidRequestCreateRequest(BaseModel):
    longitude: float
    latitude: float
    needs: list[str] = Field(default_factory=list)
    household_size: int = Field(default=1, ge=1)
    has_vulnerable_members: bool = False
    description: str = Field(..., max_length=1500)


class AidRequestUpdateRequest(BaseModel):
    status: AidRequestStatus
    assigned_to: str | None = None
