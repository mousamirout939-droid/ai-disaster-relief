from pydantic import Field

from app.models.base import MongoBaseModel


class AuditLogDocument(MongoBaseModel):
    actor_id: str
    actor_role: str
    action: str  # e.g. "incident.verify", "user.suspend", "alert.broadcast"
    resource_type: str
    resource_id: str | None = None
    metadata: dict = Field(default_factory=dict)
    ip_address: str | None = None
    user_agent: str | None = None
