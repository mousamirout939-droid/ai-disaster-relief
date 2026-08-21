"""Celery tasks for asynchronous notification delivery (SMS/push) that shouldn't block API requests."""
import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger("app.tasks.notifications")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def send_sms_notification(self, phone_number: str, message: str):
    try:
        logger.info("Sending SMS to %s", phone_number)
        # Integration point: Twilio / SNS client call goes here.
    except Exception as exc:  # noqa: BLE001 -- retry on any failure by design
        raise self.retry(exc=exc)


@celery_app.task
def send_low_stock_digest():
    """Scheduled task: aggregate low-stock shelter items and notify assigned volunteers."""
    logger.info("Running low-stock digest task.")