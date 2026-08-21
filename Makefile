.PHONY: up down build test-backend test-frontend seed migrate lint

up:
	docker compose up --build

down:
	docker compose down -v

build:
	docker compose build

test-backend:
	cd backend && pytest -v

test-frontend:
	cd frontend && npm run test

seed:
	cd backend && python scripts/seed_db.py

migrate:
	cd backend && python migrations/001_create_indexes.py && python migrations/002_seed_admin.py

lint:
	cd backend && ruff check . && black --check .
	cd frontend && npm run lint
