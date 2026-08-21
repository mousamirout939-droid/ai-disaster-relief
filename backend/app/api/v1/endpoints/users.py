from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.rbac import require_roles, require_self_or_roles
from app.repositories.user_repository import UserRepository
from app.schemas.common import PaginatedResponse
from app.schemas.user import AdminUserUpdateRequest, UserInDB, UserPublic, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"])


def get_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserRepository:
    return UserRepository(db)


@router.get("", response_model=PaginatedResponse)
async def list_users(
    page: int = 1,
    page_size: int = 20,
    role: str | None = None,
    current_user: UserInDB = Depends(require_roles("admin")),
    repo: UserRepository = Depends(get_repo),
):
    query = {"role": role} if role else {}
    items, total = await repo.paginate(query, page, page_size, sort=[("created_at", -1)])
    return PaginatedResponse.build(
        [UserPublic(**u.model_dump()).model_dump(mode="json") for u in items],
        total,
        page,
        page_size,
    )


@router.patch("/{user_id}", response_model=UserPublic)
async def update_own_profile(
    user_id: str,
    payload: UserUpdateRequest,
    current_user: UserInDB = Depends(require_self_or_roles("admin")),
    repo: UserRepository = Depends(get_repo),
):
    updated = await repo.update(user_id, payload.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
    return UserPublic(**updated.model_dump())


@router.patch("/{user_id}/admin", response_model=UserPublic)
async def admin_update_user(
    user_id: str,
    payload: AdminUserUpdateRequest,
    current_user: UserInDB = Depends(require_roles("admin")),
    repo: UserRepository = Depends(get_repo),
):
    updates = payload.model_dump(exclude_none=True)
    if "role" in updates:
        updates["role"] = updates["role"].value
    updated = await repo.update(user_id, updates)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
    return UserPublic(**updated.model_dump())