from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import decode_token
from app.dependencies.auth import get_current_active_user, oauth2_scheme
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.schemas.common import MessageResponse
from app.schemas.user import UserInDB, UserPublic
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    user = await service.register(
        payload.full_name, payload.email, payload.password, payload.phone, payload.role
    )
    return UserPublic(**user.model_dump())


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    access, refresh, _user = await service.authenticate(payload.email, payload.password)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, service: AuthService = Depends(get_auth_service)):
    access = await service.refresh_access_token(payload.refresh_token)
    return TokenResponse(access_token=access, refresh_token=payload.refresh_token)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: UserInDB = Depends(get_current_active_user),
    service: AuthService = Depends(get_auth_service),
):
    payload = decode_token(token)
    if payload:
        await service.logout(payload.jti, payload.exp)
    return MessageResponse(detail="Successfully logged out.")


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: UserInDB = Depends(get_current_active_user)):
    return UserPublic(**current_user.model_dump())