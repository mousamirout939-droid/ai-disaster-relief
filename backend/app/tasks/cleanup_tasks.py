"""Housekeeping Celery tasks: expired alert purge, stale session cleanup."""
import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger("app.tasks.cleanup")


@celery_app.task
def purge_expired_alerts():
    logger.info("Purging expired alerts (also enforced via MongoDB TTL index).")
