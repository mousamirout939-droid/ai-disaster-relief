from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies.rbac import require_roles
from app.schemas.user import UserInDB
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> AnalyticsService:
    return AnalyticsService(db)


@router.get("/dashboard")
async def get_dashboard(
    current_user: UserInDB = Depends(require_roles("admin")),
    service: AnalyticsService = Depends(get_service),
):
    return {
        "incident_summary": await service.get_incident_summary(),
        "severity_breakdown": await service.get_severity_breakdown(),
        "shelter_capacity": await service.get_shelter_capacity_overview(),
        "incidents_over_time": await service.get_incidents_over_time(),
    }
