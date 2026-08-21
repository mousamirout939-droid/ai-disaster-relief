from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.rbac import require_roles
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.shelter_repository import ShelterRepository
from app.schemas.inventory import InventoryResponse, InventoryUpdateRequest
from app.schemas.user import UserInDB
from app.services.shelter_service import ShelterService

router = APIRouter(prefix="/shelters/{shelter_id}/inventory", tags=["Inventory"])


def get_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> ShelterService:
    return ShelterService(ShelterRepository(db), InventoryRepository(db))


@router.get("", response_model=list[InventoryResponse])
async def get_inventory(shelter_id: str, service: ShelterService = Depends(get_service)):
    _, inventory = await service.get_shelter_with_inventory(shelter_id)
    return [
        InventoryResponse(id=str(i.id), is_low_stock=i.is_low_stock, **i.model_dump(exclude={"id"}))
        for i in inventory
    ]


@router.put("", response_model=InventoryResponse)
async def update_inventory(
    shelter_id: str,
    payload: InventoryUpdateRequest,
    current_user: UserInDB = Depends(require_roles("volunteer", "admin")),
    service: ShelterService = Depends(get_service),
):
    log = await service.update_inventory(
        shelter_id,
        payload.category.value,
        payload.item_name,
        payload.quantity_available,
        str(current_user.id),
        payload.unit,
    )
    return InventoryResponse(id=str(log.id), is_low_stock=log.is_low_stock, **log.model_dump(exclude={"id"}))
