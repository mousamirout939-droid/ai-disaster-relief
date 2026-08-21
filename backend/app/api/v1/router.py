"""Aggregates all v1 endpoint routers into a single APIRouter mounted by main.py."""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    aid_requests,
    alerts,
    analytics,
    audit,
    auth,
    chat,
    health,
    incidents,
    inventory,
    shelters,
    users,
    websocket,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(incidents.router)
api_router.include_router(shelters.router)
api_router.include_router(inventory.router)
api_router.include_router(alerts.router)
api_router.include_router(chat.router)
api_router.include_router(aid_requests.router)
api_router.include_router(analytics.router)
api_router.include_router(audit.router)
api_router.include_router(websocket.router)
