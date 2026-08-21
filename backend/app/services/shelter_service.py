"""Shelter + inventory coordination service used by volunteer/admin endpoints."""
import logging

from app.models.inventory import InventoryLogDocument
from app.models.shelter import ShelterDocument
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.shelter_repository import ShelterRepository

logger = logging.getLogger("app.services.shelter")


class ShelterService:
    def __init__(self, shelter_repo: ShelterRepository, inventory_repo: InventoryRepository):
        self.shelter_repo = shelter_repo
        self.inventory_repo = inventory_repo

    async def update_inventory(
        self, shelter_id: str, category: str, item_name: str, quantity_available: float, updated_by: str, unit: str = "units"
    ) -> InventoryLogDocument:
        existing = await self.inventory_repo.collection.find_one(
            {"shelter_id": shelter_id, "item_name": item_name}
        )
        if existing:
            updated = await self.inventory_repo.update(
                str(existing["_id"]),
                {"quantity_available": quantity_available, "updated_by": updated_by},
            )
            return updated
        log = InventoryLogDocument(
            shelter_id=shelter_id,
            category=category,
            item_name=item_name,
            unit=unit,
            quantity_available=quantity_available,
            updated_by=updated_by,
        )
        return await self.inventory_repo.insert(log)

    async def get_shelter_with_inventory(self, shelter_id: str) -> tuple[ShelterDocument | None, list[InventoryLogDocument]]:
        shelter = await self.shelter_repo.get_by_id(shelter_id)
        if shelter is None:
            return None, []
        inventory = await self.inventory_repo.get_by_shelter(shelter_id)
        return shelter, inventory
