"""Audit logging service — called from sensitive admin/volunteer actions for compliance trail."""
from app.models.audit_log import AuditLogDocument
from app.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, repo: AuditRepository):
        self.repo = repo

    async def log(
        self,
        actor_id: str,
        actor_role: str,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLogDocument:
        entry = AuditLogDocument(
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return await self.repo.insert(entry)
