"""
Secondary rule-based severity refinement layer, applied AFTER YOLOv8
detection to incorporate contextual signals YOLO alone can't capture
(e.g. number of corroborating citizen reports in the same area, time
since last report, category-specific baseline risk).

Kept separate from yolo_inference.py so the ML detection layer and the
business-rule layer can evolve independently.
"""
from app.models.incident import IncidentCategory, IncidentSeverity

CATEGORY_BASELINE_RISK: dict[IncidentCategory, float] = {
    IncidentCategory.EARTHQUAKE: 0.15,
    IncidentCategory.FIRE: 0.1,
    IncidentCategory.BUILDING_COLLAPSE: 0.2,
    IncidentCategory.FLOOD: 0.05,
    IncidentCategory.HURRICANE: 0.1,
    IncidentCategory.LANDSLIDE: 0.1,
    IncidentCategory.MEDICAL_EMERGENCY: 0.15,
    IncidentCategory.OTHER: 0.0,
}


def refine_severity(
    ai_confidence: float,
    ai_severity: IncidentSeverity,
    category: IncidentCategory,
    corroborating_reports_count: int,
) -> IncidentSeverity:
    score = ai_confidence + CATEGORY_BASELINE_RISK.get(category, 0.0)
    score += min(0.2, corroborating_reports_count * 0.05)

    severity_order = [IncidentSeverity.LOW, IncidentSeverity.MODERATE, IncidentSeverity.HIGH, IncidentSeverity.CRITICAL]
    base_idx = severity_order.index(ai_severity)
    if score > 0.9 and base_idx < 3:
        base_idx += 1
    return severity_order[base_idx]
