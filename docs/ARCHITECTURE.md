# System Architecture

## Overview
The platform follows a layered, service-oriented architecture within a single FastAPI
monolith (deliberately — see "Why not microservices" below), with clear domain
boundaries that allow future extraction into microservices without a rewrite.

```
Client (React PWA)
      │  HTTPS / WSS
      ▼
Nginx reverse proxy (rate limiting, TLS termination, static assets)
      │
      ▼
FastAPI application
  ├── api/v1/endpoints/*      — HTTP route handlers (thin, no business logic)
  ├── dependencies/*          — auth, RBAC, pagination (FastAPI DI)
  ├── services/*              — business logic orchestration
  ├── repositories/*          — MongoDB data access (Motor)
  ├── ml/*                    — YOLOv8 + severity scoring pipeline
  ├── websockets/*            — real-time incident/alert fan-out
  └── tasks/*                 — Celery background jobs
      │
      ├──▶ MongoDB Atlas (2dsphere geospatial indexes)
      ├──▶ Redis (cache, rate limiting, JWT blocklist, pub/sub for WS fan-out)
      ├──▶ S3-compatible object storage (incident images)
      └──▶ Google Gemini API (multilingual guidance, incident text parsing)
```

## Domain boundaries (future microservice extraction points)
- **Identity & Access** — users, auth, RBAC
- **Incident Intelligence** — incident reporting, AI severity pipeline, duplicate detection
- **Resource Coordination** — shelters, inventory, aid requests
- **Notification & Alerting** — websocket fan-out, SMS/push, admin broadcasts
- **Analytics** — aggregation pipelines for the admin dashboard

## Why a modular monolith first
At disaster-relief scale, operational simplicity and low latency between domains
(e.g. incident creation → notification) matter more than independent scaling in
the early stages. Domain modules are already decoupled via the repository/service
pattern, so any module can be extracted into its own FastAPI service later with
minimal refactor — only the dependency wiring changes.

## AI/ML Pipeline
1. Citizen uploads a photo with an incident report.
2. Image is normalized (`ml/preprocess.py`) — EXIF-corrected, downscaled, re-encoded.
3. YOLOv8 (`ml/yolo_inference.py`) detects disaster-relevant objects (fire, structural
   collapse, flood water, etc.) with confidence scores.
4. A weighted severity score (`SEVERITY_WEIGHTS`) converts detections into a
   `low | moderate | high | critical` severity band.
5. `ml/severity_classifier.py` applies a secondary rule-based refinement using
   category baseline risk and corroborating nearby reports.
6. High/critical incidents trigger real-time volunteer notification via the
   websocket connection manager (Redis pub/sub backed for multi-pod fan-out).

## Data model highlights
All location-bearing collections (`incidents`, `shelters`, `alerts`, `aid_requests`)
store a GeoJSON `Point` field and are indexed with MongoDB `2dsphere`, enabling
`$geoNear` / `$geoWithin` aggregation queries for "nearby shelters", "nearby
incidents", and geo-targeted alert broadcasts.
