from app.models.user import UserDocument
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserDocument]):
    collection_name = "users"
    model_cls = UserDocument

    async def get_by_email(self, email: str) -> UserDocument | None:
        doc = await self.collection.find_one({"email": email.lower()})
        return UserDocument(**doc) if doc else None

    async def increment_failed_login(self, email: str) -> None:
        await self.collection.update_one(
            {"email": email.lower()}, {"$inc": {"failed_login_attempts": 1}}
        )

    async def reset_failed_login(self, email: str) -> None:
        await self.collection.update_one(
            {"email": email.lower()}, {"$set": {"failed_login_attempts": 0, "locked_until": None}}
        )
