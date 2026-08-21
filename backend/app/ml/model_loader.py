"""Central model registry — warms up ML models at app startup to avoid cold-start latency on first request."""
import logging

from app.ml.yolo_inference import get_yolo_model

logger = logging.getLogger("app.ml.loader")


async def warm_up_models() -> None:
    """Called from FastAPI lifespan startup. Loads weights into memory eagerly."""
    try:
        model = get_yolo_model()
        model._load()
        logger.info("ML models warmed up successfully.")
    except Exception:
        logger.exception("Failed to warm up ML models — will lazy-load on first request instead.")
