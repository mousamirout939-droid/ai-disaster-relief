"""
Fan-out notification service: push / SMS / in-app / websocket delivery for
high-severity incident alerts and admin broadcasts. Delivery providers are
abstracted so SMS_PROVIDER / push keys can be swapped without touching
call sites.
"""
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.models.incident import IncidentDocument
from app.services.geospatial_service import GeospatialService
from app.websockets.connection_manager import connection_manager

logger = logging.getLogger("app.services.notification")


class NotificationService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def notify_nearby_volunteers(self, incident: IncidentDocument) -> None:
        lon, lat = incident.location.coordinates
        volunteers = await GeospatialService.find_nearest(
            self.db["users"],
            lon,
            lat,
            settings.ALERT_BROADCAST_RADIUS_KM,
            extra_match={"role": "volunteer", "volunteer_verified": True, "is_active": True},
        )
        payload = {
            "type": "incident.high_severity",
            "incident_id": str(incident.id),
            "category": incident.category.value,
            "severity": incident.severity.value,
            "description": incident.description[:200],
        }
        for volunteer in volunteers:
            await connection_manager.send_to_user(str(volunteer["_id"]), payload)
        logger.info("Notified %d nearby volunteers for incident %s", len(volunteers), incident.id)

    async def broadcast_alert(self, alert_doc: dict, target_user_ids: list[str] | None = None) -> None:
        if target_user_ids:
            for uid in target_user_ids:
                await connection_manager.send_to_user(uid, {"type": "alert.broadcast", **alert_doc})
        else:
            await connection_manager.broadcast({"type": "alert.broadcast", **alert_doc})
