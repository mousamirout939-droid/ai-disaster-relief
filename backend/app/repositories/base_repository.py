"""
Generic repository pattern over a Motor collection. Domain-specific
repositories inherit this to avoid re-implementing basic CRUD + pagination.
"""
from typing import Any, Generic, TypeVar

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseRepository(Generic[ModelT]):
    collection_name: str
    model_cls: type[ModelT]

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection: AsyncIOMotorCollection = db[self.collection_name]

    @staticmethod
    def to_object_id(id_str: str) -> ObjectId | None:
        try:
            return ObjectId(id_str)
        except (InvalidId, TypeError):
            return None

    async def get_by_id(self, id_str: str) -> ModelT | None:
        oid = self.to_object_id(id_str)
        if oid is None:
            return None
        doc = await self.collection.find_one({"_id": oid})
        return self.model_cls(**doc) if doc else None

    async def insert(self, model: ModelT) -> ModelT:
        payload = model.to_mongo() if hasattr(model, "to_mongo") else model.model_dump(exclude={"id"})
        result = await self.collection.insert_one(payload)
        doc = await self.collection.find_one({"_id": result.inserted_id})
        return self.model_cls(**doc)

    async def update(self, id_str: str, update_fields: dict[str, Any]) -> ModelT | None:
        oid = self.to_object_id(id_str)
        if oid is None:
            return None
        update_fields.pop("id", None)
        await self.collection.update_one({"_id": oid}, {"$set": update_fields})
        doc = await self.collection.find_one({"_id": oid})
        return self.model_cls(**doc) if doc else None

    async def delete(self, id_str: str) -> bool:
        oid = self.to_object_id(id_str)
        if oid is None:
            return False
        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count == 1

    async def paginate(
        self, query: dict, page: int = 1, page_size: int = 20, sort: list[tuple] | None = None
    ) -> tuple[list[ModelT], int]:
        skip = (page - 1) * page_size
        cursor = self.collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        cursor = cursor.skip(skip).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        total = await self.collection.count_documents(query)
        return [self.model_cls(**d) for d in docs], total
