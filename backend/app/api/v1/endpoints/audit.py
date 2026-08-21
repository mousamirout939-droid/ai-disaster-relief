from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.rbac import require_roles
from app.repositories.audit_repository import AuditRepository
from app.schemas.common import PaginatedResponse
from app.schemas.user import UserInDB

router = APIRouter(prefix="/audit-logs", tags=["Audit"])


@router.get("", response_model=PaginatedResponse)
async def list_audit_logs(
    page: int = 1,
    page_size: int = 50,
    actor_id: str | None = None,
    current_user: UserInDB = Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    repo = AuditRepository(db)
    items, total = await repo.list_recent(page, page_size, actor_id)
    return PaginatedResponse.build(
        [i.model_dump(by_alias=True, mode="json") for i in items], total, page, page_size
    )
