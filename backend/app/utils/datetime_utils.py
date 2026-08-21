from datetime import datetime, timezone


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_expired(expires_at_iso: str | None) -> bool:
    if not expires_at_iso:
        return False
    return datetime.fromisoformat(expires_at_iso) < datetime.now(timezone.utc)
