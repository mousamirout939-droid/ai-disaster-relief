"""Celery application for async background jobs (notification fan-out, cleanup, scheduled digests)."""
from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "disaster_relief_platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.notification_tasks", "app.tasks.cleanup_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "cleanup-expired-alerts": {
            "task": "app.tasks.cleanup_tasks.purge_expired_alerts",
            "schedule": 3600.0,
        },
        "low-stock-digest": {
            "task": "app.tasks.notification_tasks.send_low_stock_digest",
            "schedule": 21600.0,
        },
    },
)
