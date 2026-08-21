import logging

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness_check(db: AsyncIOMotorDatabase = Depends(get_database)):
    checks = {"mongodb": False, "redis": False}
    try:
        await db.command("ping")
        checks["mongodb"] = True
    except Exception:
        logger.warning("MongoDB health check failed", exc_info=True)
    try:
        await redis_client.ping()
        checks["redis"] = True
    except Exception:
        logger.warning("Redis health check failed", exc_info=True)
    healthy = all(checks.values())
    return {"status": "ready" if healthy else "degraded", "checks": checks}