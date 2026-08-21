"""Typed websocket event name constants shared between backend and frontend contract."""
from enum import StrEnum


class WSEvent(StrEnum):
    INCIDENT_CREATED = "incident.created"
    INCIDENT_VERIFIED = "incident.verified"
    INCIDENT_HIGH_SEVERITY = "incident.high_severity"
    SHELTER_CAPACITY_UPDATED = "shelter.capacity_updated"
    ALERT_BROADCAST = "alert.broadcast"
    AID_REQUEST_UPDATED = "aid_request.updated"
    CHAT_MESSAGE = "chat.message"
