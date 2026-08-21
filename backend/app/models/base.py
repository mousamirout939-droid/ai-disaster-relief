"""
Shared base types for MongoDB-backed domain models: ObjectId <-> str
coercion, GeoJSON Point representation, and timestamp mixins.
"""
from datetime import datetime, timezone
from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class GeoPoint(BaseModel):
    """GeoJSON Point — required shape for MongoDB 2dsphere indexes."""

    type: str = Field(default="Point", frozen=True)
    coordinates: list[float] = Field(..., min_length=2, max_length=2, description="[longitude, latitude]")

    model_config = ConfigDict(json_schema_extra={"example": {"type": "Point", "coordinates": [-122.4194, 37.7749]}})

    @property
    def longitude(self) -> float:
        return self.coordinates[0]

    @property
    def latitude(self) -> float:
        return self.coordinates[1]


class MongoBaseModel(BaseModel):
    """Base for all documents stored in MongoDB."""

    id: PyObjectId | None = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()},
    )

    def to_mongo(self, exclude_none: bool = True) -> dict[str, Any]:
        data = self.model_dump(by_alias=True, exclude_none=exclude_none, exclude={"id"})
        return data
