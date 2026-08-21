"""
Authentication service: registration, login with brute-force lockout,
token refresh, and password reset flows.
"""
import logging
from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.core.redis_client import redis_client
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import UserDocument, UserRole
from app.repositories.user_repository import UserRepository

logger = logging.getLogger("app.services.auth")

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, full_name: str, email: str, password: str, phone: str | None, role: str = "citizen") -> UserDocument:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists.")

        # Volunteers self-register but require admin approval (volunteer_verified=False)
        requested_role = UserRole.CITIZEN if role not in (UserRole.CITIZEN, UserRole.VOLUNTEER) else UserRole(role)

        user = UserDocument(
            full_name=full_name,
            email=email.lower(),
            phone=phone,
            hashed_password=hash_password(password),
            role=requested_role,
            volunteer_verified=(requested_role == UserRole.CITIZEN),
        )
        return await self.repo.insert(user)

    async def authenticate(self, email: str, password: str) -> tuple[str, str, UserDocument]:
        user = await self.repo.get_by_email(email)
        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password.")

        lock_key = f"lockout:{email.lower()}"
        if await redis_client.get(lock_key):
            raise HTTPException(status.HTTP_423_LOCKED, "Account temporarily locked due to failed attempts.")

        if not verify_password(password, user.hashed_password):
            await self.repo.increment_failed_login(email)
            if user.failed_login_attempts + 1 >= MAX_FAILED_ATTEMPTS:
                await redis_client.set(lock_key, "1", ex=LOCKOUT_MINUTES * 60)
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password.")

        if not user.is_active or user.is_suspended:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is inactive or suspended.")

        await self.repo.reset_failed_login(email)
        access = create_access_token(str(user.id), user.role.value)
        refresh = create_refresh_token(str(user.id), user.role.value)
        return access, refresh, user

    async def refresh_access_token(self, refresh_token: str) -> str:
        payload = decode_token(refresh_token)
        if payload is None or payload.type != "refresh":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token.")
        if await redis_client.exists(f"blocklist:jti:{payload.jti}"):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token has been revoked.")
        return create_access_token(payload.sub, payload.role)

    async def logout(self, jti: str, exp: int) -> None:
        ttl = max(exp - int(datetime.now(UTC).timestamp()), 1)
        await redis_client.set(f"blocklist:jti:{jti}", "1", ex=ttl)
