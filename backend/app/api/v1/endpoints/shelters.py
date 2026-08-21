from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.auth import get_current_active_user
from app.dependencies.rbac import require_roles
from app.repositories.shelter_repository import ShelterRepository
from app.schemas.shelter import ShelterCreateRequest, ShelterResponse, ShelterUpdateRequest
from app.schemas.user import UserInDB
from app.models.shelter import ShelterDocument

router = APIRouter(prefix="/shelters", tags=["Shelters"])


def get_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> ShelterRepository:
    return ShelterRepository(db)


def _to_response(s: ShelterDocument) -> ShelterResponse:
    return ShelterResponse(**s.model_dump(by_alias=True), capacity_available=s.capacity_available)


@router.post("", response_model=ShelterResponse, status_code=status.HTTP_201_CREATED)
async def create_shelter(
    payload: ShelterCreateRequest,
    current_user: UserInDB = Depends(require_roles("admin")),
    repo: ShelterRepository = Depends(get_repo),
):
    shelter = ShelterDocument(
        name=payload.name,
        shelter_type=payload.shelter_type,
        location={"type": "Point", "coordinates": [payload.longitude, payload.latitude]},
        address_text=payload.address_text,
        capacity_total=payload.capacity_total,
        contact_phone=payload.contact_phone,
        accessibility_features=payload.accessibility_features,
        managed_by=str(current_user.id),
    )
    saved = await repo.insert(shelter)
    return _to_response(saved)


@router.get("/nearby", response_model=list[ShelterResponse])
async def get_nearby_shelters(
    longitude: float,
    latitude: float,
    radius_km: float = 25.0,
    shelter_type: str | None = None,
    repo: ShelterRepository = Depends(get_repo),
):
    shelters = await repo.find_near(longitude, latitude, radius_km, shelter_type)
    return [_to_response(s) for s in shelters]


@router.get("/{shelter_id}", response_model=ShelterResponse)
async def get_shelter(shelter_id: str, repo: ShelterRepository = Depends(get_repo)):
    shelter = await repo.get_by_id(shelter_id)
    if not shelter:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Shelter not found.")
    return _to_response(shelter)


@router.patch("/{shelter_id}", response_model=ShelterResponse)
async def update_shelter(
    shelter_id: str,
    payload: ShelterUpdateRequest,
    current_user: UserInDB = Depends(require_roles("volunteer", "admin")),
    repo: ShelterRepository = Depends(get_repo),
):
    updates = payload.model_dump(exclude_none=True)
    shelter = await repo.update(shelter_id, updates)
    if not shelter:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Shelter not found.")
    return _to_response(shelter)


@router.delete("/{shelter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelter(
    shelter_id: str,
    current_user: UserInDB = Depends(require_roles("admin")),
    repo: ShelterRepository = Depends(get_repo),
):
    deleted = await repo.delete(shelter_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Shelter not found.")
