from pydantic import Field

from app.models.base import MongoBaseModel


class ChatMessageDocument(MongoBaseModel):
    session_id: str
    user_id: str
    role: str  # "user" | "assistant"
    content: str = Field(..., max_length=8000)
    detected_language: str | None = None
    grounded_sources: list[str] = Field(default_factory=list)
