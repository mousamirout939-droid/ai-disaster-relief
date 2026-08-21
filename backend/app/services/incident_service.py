"""
Incident domain service: coordinates image storage, AI severity analysis
(YOLOv8 + optional Gemini text parsing), duplicate detection, and
persistence. This is the core orchestration layer invoked by the
incidents API endpoints — kept separate from the route handlers so the
same logic can be reused by background tasks / websocket handlers.
"""
import logging
from datetime import UTC

from app.ml.yolo_inference import analyze_image_severity
from app.models.incident import (
    AISeverityAnalysis,
    IncidentDocument,
    IncidentSeverity,
    IncidentStatus,
)
from app.repositories.incident_repository import IncidentRepository
from app.services.gemini_service import GeminiService
from app.services.notification_service import NotificationService
from app.services.storage_service import StorageService

logger = logging.getLogger("app.services.incident")


class IncidentService:
    def __init__(self, repo: IncidentRepository, storage: StorageService, notifier: NotificationService):
        self.repo = repo
        self.storage = storage
        self.notifier = notifier

    async def create_incident(
        self,
        reported_by: str,
        category: str,
        description: str,
        longitude: float,
        latitude: float,
        image_bytes_list: list[bytes],
        image_filenames: list[str],
        address_text: str | None = None,
    ) -> IncidentDocument:
        # 1. Upload images to object storage
        image_urls: list[str] = []
        for content, filename in zip(image_bytes_list, image_filenames):
            url = await self.storage.upload_file(content, filename, folder="incidents")
            image_urls.append(url)

        # 2. Run AI severity analysis on the first image (primary evidence)
        ai_analysis: AISeverityAnalysis | None = None
        severity = IncidentSeverity.MODERATE
        if image_urls:
            local_path = await self.storage.get_local_path_for_inference(image_urls[0])
            analysis_result = await analyze_image_severity(local_path)
            ai_analysis = AISeverityAnalysis(**analysis_result)
            severity = IncidentSeverity(analysis_result["predicted_severity"])
        else:
            # No image — fall back to Gemini text-based urgency hint
            parsed = await GeminiService.parse_incident_text(description)
            severity = IncidentSeverity(parsed.get("urgency_hint", "moderate"))

        # 3. Duplicate detection — warn but do not block submission
        duplicates = await self.repo.find_potential_duplicates(longitude, latitude, category)

        incident = IncidentDocument(
            reported_by=reported_by,
            category=category,
            description=description,
            location={"type": "Point", "coordinates": [longitude, latitude]},
            address_text=address_text,
            image_urls=image_urls,
            ai_analysis=ai_analysis,
            severity=severity,
            status=IncidentStatus.PENDING_REVIEW,
            duplicate_of=str(duplicates[0].id) if duplicates else None,
        )
        saved = await self.repo.insert(incident)

        # 4. Notify nearby volunteers for high/critical severity incidents
        if severity in (IncidentSeverity.HIGH, IncidentSeverity.CRITICAL):
            await self.notifier.notify_nearby_volunteers(saved)

        logger.info(
            "Incident created id=%s severity=%s duplicates=%d",
            saved.id,
            severity.value,
            len(duplicates),
        )
        return saved

    async def verify_incident(self, incident_id: str, verifier_id: str, approve: bool) -> IncidentDocument | None:
        from datetime import datetime

        new_status = IncidentStatus.VERIFIED if approve else IncidentStatus.REJECTED
        return await self.repo.update(
            incident_id,
            {
                "status": new_status.value,
                "verified_by": verifier_id,
                "verified_at": datetime.now(UTC).isoformat(),
            },
        )

    async def get_nearby(self, longitude: float, latitude: float, radius_km: float, status: str | None):
        return await self.repo.find_near(longitude, latitude, radius_km, status)
