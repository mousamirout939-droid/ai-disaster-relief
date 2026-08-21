"""Alert broadcasting service: admin-triggered emergency alerts, geo-targeted or platform-wide."""
import logging

from app.models.alert import AlertDocument
from app.repositories.alert_repository import AlertRepository
from app.services.notification_service import NotificationService

logger = logging.getLogger("app.services.alert")


class AlertService:
    def __init__(self, repo: AlertRepository, notifier: NotificationService):
        self.repo = repo
        self.notifier = notifier

    async def broadcast(
        self,
        issued_by: str,
        title: str,
        message: str,
        severity: str,
        longitude: float | None = None,
        latitude: float | None = None,
        radius_km: float | None = None,
        expires_at: str | None = None,
    ) -> AlertDocument:
        location = {"type": "Point", "coordinates": [longitude, latitude]} if longitude is not None else None
        alert = AlertDocument(
            title=title,
            message=message,
            severity=severity,
            issued_by=issued_by,
            location=location,
            radius_km=radius_km,
            expires_at=expires_at,
        )
        saved = await self.repo.insert(alert)
        await self.notifier.broadcast_alert(saved.model_dump(mode="json"))
        logger.info("Alert broadcast id=%s severity=%s geo_targeted=%s", saved.id, severity, bool(location))
        return saved
