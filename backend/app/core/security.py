"""
Cryptographic and authentication primitives: password hashing (Argon2/bcrypt
via passlib), JWT access/refresh token issuance and verification.
"""
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
    PASSWORD_RESET = "password_reset"


class TokenPayload(BaseModel):
    sub: str  # user id
    role: str
    type: TokenType
    exp: int
    iat: int
    jti: str


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(subject: str, role: str, token_type: TokenType, expires_delta: timedelta) -> str:
    import uuid

    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "role": role,
        "type": token_type.value,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str, role: str) -> str:
    return _create_token(
        user_id, role, TokenType.ACCESS, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user_id: str, role: str) -> str:
    return _create_token(
        user_id, role, TokenType.REFRESH, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def create_password_reset_token(user_id: str, role: str) -> str:
    return _create_token(
        user_id,
        role,
        TokenType.PASSWORD_RESET,
        timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
    )


def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        raw: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return TokenPayload(**raw)
    except (JWTError, ValueError):
        return None
