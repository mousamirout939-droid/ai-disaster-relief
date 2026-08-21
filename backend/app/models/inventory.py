from enum import StrEnum

from pydantic import Field

from app.models.base import MongoBaseModel


class SupplyCategory(StrEnum):
    FOOD = "food"
    WATER = "water"
    MEDICAL = "medical"
    BEDDING = "bedding"
    HYGIENE = "hygiene"
    CLOTHING = "clothing"
    OTHER = "other"


class InventoryLogDocument(MongoBaseModel):
    shelter_id: str
    category: SupplyCategory
    item_name: str
    unit: str = "units"  # e.g. "liters", "kg", "units"
    quantity_available: float = Field(ge=0)
    quantity_threshold_low: float = Field(default=10, ge=0)
    updated_by: str  # volunteer/admin user id
    notes: str | None = None

    @property
    def is_low_stock(self) -> bool:
        return self.quantity_available <= self.quantity_threshold_low
