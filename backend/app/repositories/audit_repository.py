from app.models.audit_log import AuditLogDocument
from app.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository[AuditLogDocument]):
    collection_name = "audit_logs"
    model_cls = AuditLogDocument

    async def list_recent(self, page: int = 1, page_size: int = 50, actor_id: str | None = None):
        query = {"actor_id": actor_id} if actor_id else {}
        return await self.paginate(query, page, page_size, sort=[("created_at", -1)])
