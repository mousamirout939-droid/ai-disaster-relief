from enum import StrEnum
from typing import Optional

from pydantic import EmailStr, Field

from app.models.base import GeoPoint, MongoBaseModel


class UserRole(StrEnum):
    CITIZEN = "citizen"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"


class UserDocument(MongoBaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    hashed_password: str
    role: UserRole = UserRole.CITIZEN
    is_active: bool = True
    is_suspended: bool = False
    is_email_verified: bool = False
    preferred_language: str = "en"
    last_known_location: Optional[GeoPoint] = None
    volunteer_verified: bool = False  # admin must approve volunteer status
    organization: Optional[str] = None  # e.g. Red Cross, local NGO
    notification_preferences: dict = Field(
        default_factory=lambda: {"sms": True, "push": True, "email": True}
    )
    failed_login_attempts: int = 0
    locked_until: Optional[str] = None
