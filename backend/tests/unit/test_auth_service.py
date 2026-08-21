import pytest
from fastapi import HTTPException

from app.core.security import hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_password_hash_and_verify_roundtrip():
    plain = "SuperSecret123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong-password", hashed) is False


@pytest.mark.asyncio
async def test_register_creates_citizen_by_default(mock_db):
    repo = UserRepository(mock_db)
    service = AuthService(repo)
    user = await service.register("Jane Doe", "jane@example.com", "SuperSecret123", None)
    assert user.role.value == "citizen"
    assert user.email == "jane@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_email_raises(mock_db):
    repo = UserRepository(mock_db)
    service = AuthService(repo)
    await service.register("Jane Doe", "dupe@example.com", "SuperSecret123", None)
    with pytest.raises(HTTPException):
        await service.register("Jane Doe 2", "dupe@example.com", "SuperSecret123", None)