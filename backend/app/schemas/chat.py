from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(..., min_length=1, max_length=4000)


class ChatMessageResponse(BaseModel):
    session_id: str
    reply: str
    detected_language: str | None = None
