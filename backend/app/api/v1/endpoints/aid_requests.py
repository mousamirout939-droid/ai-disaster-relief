from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.auth import get_current_active_user
from app.dependencies.rbac import require_roles
from app.models.aid_request import AidRequestDocument
from app.repositories.base_repository import BaseRepository
from app.schemas.aid_request import AidRequestCreateRequest, AidRequestUpdateRequest
from app.schemas.user import UserInDB

router = APIRouter(prefix="/aid-requests", tags=["Aid Requests"])


class AidRequestRepository(BaseRepository[AidRequestDocument]):
    collection_name = "aid_requests"
    model_cls = AidRequestDocument


def get_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> AidRequestRepository:
    return AidRequestRepository(db)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_aid_request(
    payload: AidRequestCreateRequest,
    current_user: UserInDB = Depends(get_current_active_user),
    repo: AidRequestRepository = Depends(get_repo),
):
    doc = AidRequestDocument(
        requested_by=str(current_user.id),
        location={"type": "Point", "coordinates": [payload.longitude, payload.latitude]},
        needs=payload.needs,
        household_size=payload.household_size,
        has_vulnerable_members=payload.has_vulnerable_members,
        description=payload.description,
    )
    saved = await repo.insert(doc)
    return saved.model_dump(by_alias=True, mode="json")


@router.patch("/{request_id}")
async def update_aid_request(
    request_id: str,
    payload: AidRequestUpdateRequest,
    current_user: UserInDB = Depends(require_roles("volunteer", "admin")),
    repo: AidRequestRepository = Depends(get_repo),
):
    updated = await repo.update(request_id, payload.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aid request not found.")
    return updated.model_dump(by_alias=True, mode="json")
