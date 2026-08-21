
from app.ml.severity_classifier import refine_severity
from app.models.incident import IncidentCategory, IncidentSeverity


def test_refine_severity_escalates_with_corroboration():
    base = refine_severity(0.6, IncidentSeverity.MODERATE, IncidentCategory.FIRE, 0)
    escalated = refine_severity(0.6, IncidentSeverity.MODERATE, IncidentCategory.FIRE, 10)
    order = [IncidentSeverity.LOW, IncidentSeverity.MODERATE, IncidentSeverity.HIGH, IncidentSeverity.CRITICAL]
    assert order.index(escalated) >= order.index(base)


def test_refine_severity_never_exceeds_critical():
    result = refine_severity(1.0, IncidentSeverity.CRITICAL, IncidentCategory.EARTHQUAKE, 100)
    assert result == IncidentSeverity.CRITICAL
