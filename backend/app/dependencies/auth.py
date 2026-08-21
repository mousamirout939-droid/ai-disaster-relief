"""
Authentication dependency chain: extracts and validates the bearer JWT,
loads the user from MongoDB, and ensures the account is active and not
soft-deleted. Also checks a Redis-backed token blocklist for revoked tokens
(logout / password change invalidation).
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.redis_client import redis_client
from app.core.security import TokenType, decode_token
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=True)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> UserInDB:
    payload = decode_token(token)
    if payload is None or payload.type != TokenType.ACCESS:
        raise CREDENTIALS_EXCEPTION

    # Reject tokens that were explicitly revoked (logout / password reset)
    if await redis_client.exists(f"blocklist:jti:{payload.jti}"):
        raise CREDENTIALS_EXCEPTION

    repo = UserRepository(db)
    user = await repo.get_by_id(payload.sub)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated.")
    if current_user.is_suspended:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is suspended.")
    return current_user


async def get_optional_user(
    token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> UserInDB | None:
    """For endpoints that behave differently for anonymous vs authenticated users."""
    if not token:
        return None
    payload = decode_token(token)
    if payload is None or payload.type != TokenType.ACCESS:
        return None
    repo = UserRepository(db)
    return await repo.get_by_id(payload.sub)
