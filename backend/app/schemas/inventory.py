from pydantic import BaseModel, Field

from app.models.inventory import SupplyCategory


class InventoryUpdateRequest(BaseModel):
    category: SupplyCategory
    item_name: str = Field(..., min_length=1, max_length=100)
    quantity_available: float = Field(ge=0)
    unit: str = "units"


class InventoryResponse(BaseModel):
    id: str
    shelter_id: str
    category: SupplyCategory
    item_name: str
    unit: str
    quantity_available: float
    is_low_stock: bool
