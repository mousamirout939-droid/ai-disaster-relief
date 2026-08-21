from app.models.inventory import InventoryLogDocument
from app.repositories.base_repository import BaseRepository


class InventoryRepository(BaseRepository[InventoryLogDocument]):
    collection_name = "inventory_logs"
    model_cls = InventoryLogDocument

    async def get_by_shelter(self, shelter_id: str) -> list[InventoryLogDocument]:
        cursor = self.collection.find({"shelter_id": shelter_id}).sort("category", 1)
        docs = await cursor.to_list(length=500)
        return [InventoryLogDocument(**d) for d in docs]

    async def get_low_stock(self) -> list[InventoryLogDocument]:
        cursor = self.collection.find(
            {"$expr": {"$lte": ["$quantity_available", "$quantity_threshold_low"]}}
        )
        docs = await cursor.to_list(length=1000)
        return [InventoryLogDocument(**d) for d in docs]
