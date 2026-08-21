from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.base import PyObjectId
from app.models.user import UserRole


class UserInDB(BaseModel):
    id: PyObjectId
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    hashed_password: str
    role: UserRole
    is_active: bool
    is_suspended: bool
    volunteer_verified: bool
    created_at: datetime

    model_config = ConfigDict(populate_by_name=True)


class UserPublic(BaseModel):
    id: PyObjectId
    full_name: str
    email: EmailStr
    role: UserRole
    organization: Optional[str] = None
    volunteer_verified: bool

    model_config = ConfigDict(populate_by_name=True)


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: Optional[str] = None
    notification_preferences: Optional[dict] = None


class AdminUserUpdateRequest(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_suspended: Optional[bool] = None
    volunteer_verified: Optional[bool] = None
