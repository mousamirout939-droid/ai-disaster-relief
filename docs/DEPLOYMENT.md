# Deployment Guide

## Local development
```bash
cp .env.example .env
make up        # docker compose up --build
make migrate   # index creation + admin seed
```

## Staging / Production (Kubernetes)
1. Provision infra with Terraform:
   ```bash
   cd infra/terraform
   terraform init
   terraform apply -var="atlas_org_id=<your-atlas-org-id>"
   ```
2. Build & push images (handled automatically by `.github/workflows/deploy-prod.yml`
   on merge to `main`), or manually:
   ```bash
   docker build -t ghcr.io/org/disaster-relief-backend:latest ./backend
   docker build -t ghcr.io/org/disaster-relief-frontend:latest ./frontend
   docker push ghcr.io/org/disaster-relief-backend:latest
   docker push ghcr.io/org/disaster-relief-frontend:latest
   ```
3. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f infra/k8s/namespace.yaml
   kubectl apply -f infra/k8s/configmap.yaml
   kubectl apply -f infra/k8s/secrets.yaml   # populated from secrets.yaml.example
   kubectl apply -f infra/k8s/
   ```
4. Verify rollout:
   ```bash
   kubectl rollout status deployment/backend -n disaster-relief
   kubectl get hpa -n disaster-relief
   ```

## Observability
- Prometheus scrapes `/metrics` on the backend (`prometheus-fastapi-instrumentator`).
- Grafana dashboards are auto-provisioned from `infra/monitoring/grafana/`.
- Structured JSON logs in production (`app/core/logging_config.py`) are
  designed for direct ingestion into CloudWatch Logs / ELK / Loki.

## Secrets management
Never commit populated `secrets.yaml` or `.env` files. Use `secrets.yaml.example`
as a template and inject real values via your cluster's secret manager
(AWS Secrets Manager + External Secrets Operator, Sealed Secrets, or Vault).

## Database migrations
Index creation is idempotent and runs automatically on backend startup
(`app.core.database.MongoDatabase._ensure_indexes`), but can also be run
explicitly and audited via `backend/migrations/`:
```bash
python backend/migrations/001_create_indexes.py
python backend/migrations/002_seed_admin.py
python backend/migrations/003_geospatial_indexes.py   # verification only
```
