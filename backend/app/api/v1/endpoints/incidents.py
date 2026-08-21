from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.constants import MAX_IMAGES_PER_INCIDENT, SUPPORTED_IMAGE_TYPES
from app.core.database import get_database
from app.dependencies.auth import get_current_active_user
from app.dependencies.rbac import require_roles
from app.ml.preprocess import normalize_image, validate_image_bytes
from app.repositories.audit_repository import AuditRepository
from app.repositories.incident_repository import IncidentRepository
from app.schemas.common import PaginatedResponse
from app.schemas.incident import IncidentCreateRequest, IncidentResponse, IncidentVerifyRequest
from app.schemas.user import UserInDB
from app.services.audit_service import AuditService
from app.services.incident_service import IncidentService
from app.services.notification_service import NotificationService
from app.services.storage_service import StorageService

router = APIRouter(prefix="/incidents", tags=["Incidents"])


def get_incident_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> IncidentService:
    return IncidentService(IncidentRepository(db), StorageService(), NotificationService(db))


def get_audit_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> AuditService:
    return AuditService(AuditRepository(db))


@router.post("", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def report_incident(
    category: str = Form(...),
    description: str = Form(...),
    longitude: float = Form(...),
    latitude: float = Form(...),
    address_text: str | None = Form(None),
    images: list[UploadFile] = File(default=[]),
    current_user: UserInDB = Depends(get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
):
    if len(images) > MAX_IMAGES_PER_INCIDENT:
        raise HTTPException(400, f"Maximum {MAX_IMAGES_PER_INCIDENT} images allowed per report.")

    image_bytes_list, filenames = [], []
    for image in images:
        if image.content_type not in SUPPORTED_IMAGE_TYPES:
            raise HTTPException(400, f"Unsupported image type: {image.content_type}")
        raw = await image.read()
        validate_image_bytes(raw)
        image_bytes_list.append(normalize_image(raw))
        filenames.append(image.filename or "upload.jpg")

    incident = await service.create_incident(
        reported_by=str(current_user.id),
        category=category,
        description=description,
        longitude=longitude,
        latitude=latitude,
        image_bytes_list=image_bytes_list,
        image_filenames=filenames,
        address_text=address_text,
    )
    return IncidentResponse(**incident.model_dump(by_alias=True))


@router.get("/nearby", response_model=list[IncidentResponse])
async def get_nearby_incidents(
    longitude: float,
    latitude: float,
    radius_km: float = 25.0,
    status_filter: str | None = None,
    current_user: UserInDB = Depends(get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
):
    incidents = await service.get_nearby(longitude, latitude, radius_km, status_filter)
    return [IncidentResponse(**i.model_dump(by_alias=True)) for i in incidents]


@router.get("", response_model=PaginatedResponse)
async def list_incidents(
    page: int = 1,
    page_size: int = 20,
    status_filter: str | None = None,
    repo: IncidentRepository = Depends(lambda db=Depends(get_database): IncidentRepository(db)),
):
    query = {"status": status_filter} if status_filter else {}
    items, total = await repo.paginate(query, page, page_size, sort=[("created_at", -1)])
    return PaginatedResponse.build(
        [IncidentResponse(**i.model_dump(by_alias=True)) for i in items], total, page, page_size
    )


@router.post("/{incident_id}/verify", response_model=IncidentResponse)
async def verify_incident(
    incident_id: str,
    payload: IncidentVerifyRequest,
    current_user: UserInDB = Depends(require_roles("volunteer", "admin")),
    service: IncidentService = Depends(get_incident_service),
    audit: AuditService = Depends(get_audit_service),
):
    incident = await service.verify_incident(incident_id, str(current_user.id), payload.approve)
    if incident is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incident not found.")
    await audit.log(
        actor_id=str(current_user.id),
        actor_role=current_user.role.value,
        action="incident.verify" if payload.approve else "incident.reject",
        resource_type="incident",
        resource_id=incident_id,
        metadata={"notes": payload.notes},
    )
    return IncidentResponse(**incident.model_dump(by_alias=True))
