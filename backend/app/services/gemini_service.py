"""
Google Gemini integration for the multilingual AI emergency assistant.

Responsibilities:
  1. Answer citizen emergency-guidance questions (first aid, evacuation,
     shelter-in-place instructions) grounded in a safety system prompt.
  2. Auto-detect / translate across languages so non-native speakers get
     guidance in their own language.
  3. Parse free-text incident descriptions into structured category +
     urgency hints to assist (not replace) the YOLO severity pipeline.

Safety: the system prompt hard-constrains the model to defer to human
emergency services for anything life-threatening and never to give medical
dosing, evacuation routes it cannot verify, or discourage calling emergency
services.
"""
import json
import logging

import google.generativeai as genai

from app.core.config import settings

logger = logging.getLogger("app.services.gemini")

SYSTEM_PROMPT = """You are the AI Emergency Assistant for a disaster relief platform.
Rules you must always follow:
1. If the user describes an immediate life-threatening emergency, your FIRST
   line must urge them to contact local emergency services immediately.
2. Give clear, calm, step-by-step safety guidance (e.g., what to do during an
   earthquake, flood, or fire) using widely-accepted public safety guidance.
3. Never provide medical dosing instructions or diagnose conditions.
4. Respond in the same language the user wrote in, unless they ask otherwise.
5. Keep responses concise and actionable — this may be read during a crisis.
6. If unsure or the question is outside disaster/safety scope, say so plainly.
"""

_model = None


def _get_model():
    global _model
    if _model is None:
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set — AI assistant will return a fallback message.")
            return None
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )
    return _model


class GeminiService:
    @staticmethod
    async def get_emergency_guidance(user_message: str, conversation_history: list[dict] | None = None) -> dict:
        model = _get_model()
        if model is None:
            return {
                "reply": "The AI assistant is temporarily unavailable. For any life-threatening "
                "emergency, please contact your local emergency services immediately.",
                "detected_language": "unknown",
            }

        history = []
        for turn in conversation_history or []:
            role = "user" if turn.get("role") == "user" else "model"
            history.append({"role": role, "parts": [turn.get("content", "")]})

        chat = model.start_chat(history=history)
        response = await chat.send_message_async(user_message)
        return {"reply": response.text, "detected_language": None}

    @staticmethod
    async def parse_incident_text(free_text: str) -> dict:
        """
        Uses Gemini structured output to extract category/urgency hints from
        a free-text incident report, to complement image-based YOLO analysis
        (e.g. when no photo is available).
        """
        model = _get_model()
        if model is None:
            return {"category_hint": "other", "urgency_hint": "moderate", "extracted_needs": []}

        prompt = (
            "Extract structured info from this disaster report as strict JSON with keys "
            "category_hint (one of: flood, fire, earthquake, hurricane, landslide, "
            "building_collapse, medical_emergency, other), urgency_hint (low, moderate, high, "
            "critical), and extracted_needs (array of strings like 'food','water','medical',"
            "'rescue','shelter'). Report:\n\n" + free_text
        )
        response = await model.generate_content_async(
            prompt, generation_config={"response_mime_type": "application/json"}
        )
        try:
            return json.loads(response.text)
        except (json.JSONDecodeError, AttributeError):
            logger.warning("Gemini structured parse failed, returning defaults.")
            return {"category_hint": "other", "urgency_hint": "moderate", "extracted_needs": []}
