import uuid

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.auth import get_current_active_user
from app.models.chat import ChatMessageDocument
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.schemas.user import UserInDB
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/chat", tags=["AI Assistant"])


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    payload: ChatMessageRequest,
    current_user: UserInDB = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    session_id = payload.session_id or str(uuid.uuid4())

    history_cursor = db["chat_sessions"].find({"session_id": session_id}).sort("created_at", 1).limit(20)
    history = [{"role": m["role"], "content": m["content"]} async for m in history_cursor]

    result = await GeminiService.get_emergency_guidance(payload.message, history)

    user_msg = ChatMessageDocument(session_id=session_id, user_id=str(current_user.id), role="user", content=payload.message)
    assistant_msg = ChatMessageDocument(
        session_id=session_id, user_id=str(current_user.id), role="assistant", content=result["reply"]
    )
    await db["chat_sessions"].insert_one(user_msg.to_mongo())
    await db["chat_sessions"].insert_one(assistant_msg.to_mongo())

    return ChatMessageResponse(session_id=session_id, reply=result["reply"], detected_language=result.get("detected_language"))
