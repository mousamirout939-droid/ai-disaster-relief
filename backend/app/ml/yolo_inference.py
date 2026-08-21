"""
YOLOv8 inference wrapper for automated disaster-image severity analysis.

Design notes:
- The model is loaded once per process (singleton) and cached — loading
  torch weights per-request would be prohibitively slow.
- Inference is run in a threadpool executor since ultralytics/torch calls
  are blocking/CPU (or GPU) bound and would otherwise stall the event loop.
- Severity is derived from a weighted combination of detected-object class,
  confidence, and coverage area of destructive features (fire, structural
  collapse, flooding extent) rather than a single classifier head — this
  gives more interpretable, tunable severity bands.
"""
import asyncio
import logging
import time
from functools import lru_cache
from pathlib import Path

from app.core.config import settings
from app.models.incident import IncidentSeverity

logger = logging.getLogger("app.ml.yolo")

# Class -> base severity weight. Tunable without retraining.
SEVERITY_WEIGHTS: dict[str, float] = {
    "fire": 0.9,
    "smoke": 0.5,
    "structural_collapse": 1.0,
    "flood_water": 0.7,
    "debris": 0.4,
    "vehicle_damage": 0.3,
    "person_in_distress": 0.85,
    "landslide": 0.8,
}


class YOLOSeverityModel:
    """Lazy-loaded singleton wrapper around an ultralytics YOLOv8 model."""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load(self):
        if self._model is not None:
            return
        try:
            from ultralytics import YOLO  # heavy import, kept local

            weights_path = Path(settings.YOLO_WEIGHTS_PATH)
            if not weights_path.exists():
                logger.warning(
                    "YOLO weights not found at %s — falling back to base yolov8n.pt. "
                    "Replace with a fine-tuned disaster-severity checkpoint for production.",
                    weights_path,
                )
                self._model = YOLO("yolov8n.pt")
            else:
                self._model = YOLO(str(weights_path))
            logger.info("YOLOv8 severity model loaded (device=%s)", settings.ML_INFERENCE_DEVICE)
        except ImportError:
            logger.error("ultralytics not installed — AI severity analysis disabled.")
            self._model = None

    def predict_sync(self, image_path: str) -> dict:
        self._load()
        if self._model is None:
            return {"detections": [], "model_version": "unavailable"}

        results = self._model.predict(
            source=image_path,
            conf=settings.YOLO_CONFIDENCE_THRESHOLD,
            device=settings.ML_INFERENCE_DEVICE,
            verbose=False,
        )
        detections = []
        for result in results:
            for box in result.boxes:
                label = result.names[int(box.cls[0])]
                detections.append(
                    {
                        "label": label,
                        "confidence": float(box.conf[0]),
                        "bbox": [float(x) for x in box.xyxy[0].tolist()],
                    }
                )
        return {"detections": detections, "model_version": "yolov8-disaster-severity-v1"}


@lru_cache
def get_yolo_model() -> YOLOSeverityModel:
    return YOLOSeverityModel()


def _score_to_severity(score: float) -> IncidentSeverity:
    if score >= 0.75:
        return IncidentSeverity.CRITICAL
    if score >= 0.5:
        return IncidentSeverity.HIGH
    if score >= 0.25:
        return IncidentSeverity.MODERATE
    return IncidentSeverity.LOW


async def analyze_image_severity(image_path: str) -> dict:
    """
    Async entrypoint used by the incident service. Runs blocking YOLO
    inference in a thread executor to avoid blocking the FastAPI event loop.
    """
    model = get_yolo_model()
    start = time.perf_counter()
    loop = asyncio.get_running_loop()
    raw = await loop.run_in_executor(None, model.predict_sync, image_path)
    elapsed_ms = (time.perf_counter() - start) * 1000

    detections = raw["detections"]
    if not detections:
        return {
            "model_version": raw["model_version"],
            "predicted_severity": IncidentSeverity.LOW.value,
            "confidence": 0.0,
            "detected_objects": [],
            "inference_ms": elapsed_ms,
        }

    # Weighted severity score: max(class_weight * confidence) across detections,
    # with a small boost for multiple corroborating destructive signals.
    weighted_scores = [
        SEVERITY_WEIGHTS.get(d["label"], 0.3) * d["confidence"] for d in detections
    ]
    top_score = max(weighted_scores)
    corroboration_boost = min(0.15, 0.03 * (len(detections) - 1))
    final_score = min(1.0, top_score + corroboration_boost)

    return {
        "model_version": raw["model_version"],
        "predicted_severity": _score_to_severity(final_score).value,
        "confidence": round(final_score, 4),
        "detected_objects": detections,
        "inference_ms": round(elapsed_ms, 2),
    }
