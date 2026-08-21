"""Minimal server-side i18n helper for system-generated notification strings (UI translations live in frontend/src/i18n)."""
from app.core.constants import SUPPORTED_LANGUAGES

FALLBACK_LANGUAGE = "en"

NOTIFICATION_STRINGS = {
    "en": {"high_severity_incident": "A high-severity incident was reported near you."},
    "es": {"high_severity_incident": "Se reportó un incidente de alta gravedad cerca de usted."},
    "fr": {"high_severity_incident": "Un incident de gravité élevée a été signalé près de chez vous."},
}


def translate(key: str, language: str = FALLBACK_LANGUAGE) -> str:
    lang = language if language in SUPPORTED_LANGUAGES else FALLBACK_LANGUAGE
    return NOTIFICATION_STRINGS.get(lang, NOTIFICATION_STRINGS[FALLBACK_LANGUAGE]).get(
        key, NOTIFICATION_STRINGS[FALLBACK_LANGUAGE].get(key, key)
    )
