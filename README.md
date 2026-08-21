# AI Disaster Relief & Rescue Platform

A production-grade, AI-powered platform for real-time disaster reporting, shelter/resource
coordination, and multilingual emergency guidance — built for citizens, volunteers, and
disaster-response administrators.

## Architecture

- **Frontend**: React 18 (Vite) + Tailwind CSS + Leaflet.js + Zustand, offline-first PWA
- **Backend**: FastAPI (async), Motor (MongoDB async ODM), Redis caching/rate-limiting
- **AI/ML**: YOLOv8 disaster-image severity analysis, Google Gemini multilingual assistant
- **Infra**: Docker Compose (dev), Kubernetes + Terraform (prod), GitHub Actions CI/CD,
  Nginx reverse proxy, Prometheus + Grafana monitoring

See `docs/ARCHITECTURE.md`, `docs/RBAC_MATRIX.md`, `docs/API_SPEC.md`, and
`docs/DEPLOYMENT.md` for full detail.

## Quick start (local development)

```bash
cp .env.example .env          # fill in GEMINI_API_KEY etc.
make up                       # docker compose up --build
make migrate                  # create indexes + seed admin account
make seed                     # optional: sample shelters for local testing
```

- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/api/v1/docs
- Grafana: http://localhost:3000

## Repository layout

```
backend/    FastAPI service, ML pipeline, repositories, tests, migrations
frontend/   React PWA client
infra/      Docker, Kubernetes manifests, Terraform IaC, monitoring config
.github/    CI/CD workflows
docs/       Architecture, API, RBAC, and deployment documentation
```

## RBAC summary

| Role       | Capabilities                                                                 |
|------------|-------------------------------------------------------------------------------|
| Citizen    | Report incidents, view shelters/alerts, chat with AI assistant, request aid  |
| Volunteer  | + Verify incidents, manage shelter inventory, coordinate distribution        |
| Admin      | + Full CRUD on users/incidents/shelters, broadcast alerts, audit log access  |

## License

MIT — see `LICENSE`.
