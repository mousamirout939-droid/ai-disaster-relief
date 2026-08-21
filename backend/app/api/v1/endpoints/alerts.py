from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.rbac import require_roles
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import AlertBroadcastRequest
from app.schemas.user import UserInDB
from app.services.alert_service import AlertService
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/alerts", tags=["Alerts"])


def get_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> AlertService:
    return AlertService(AlertRepository(db), NotificationService(db))


@router.post("/broadcast")
async def broadcast_alert(
    payload: AlertBroadcastRequest,
    current_user: UserInDB = Depends(require_roles("admin")),
    service: AlertService = Depends(get_service),
):
    alert = await service.broadcast(
        issued_by=str(current_user.id),
        title=payload.title,
        message=payload.message,
        severity=payload.severity.value,
        longitude=payload.longitude,
        latitude=payload.latitude,
        radius_km=payload.radius_km,
        expires_at=payload.expires_at,
    )
    return alert.model_dump(by_alias=True, mode="json")


@router.get("/nearby")
async def get_nearby_alerts(
    longitude: float,
    latitude: float,
    radius_km: float = 50.0,
    repo: AlertRepository = Depends(lambda db=Depends(get_database): AlertRepository(db)),
):
    alerts = await repo.find_active_near(longitude, latitude, radius_km)
    return [a.model_dump(by_alias=True, mode="json") for a in alerts]
