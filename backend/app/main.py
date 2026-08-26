"""
Application entrypoint. Wires together lifespan-managed resources (MongoDB,
Redis pub/sub listener, ML model warm-up), middleware stack, exception
handlers, and the versioned API router.

Run with: uvicorn app.main:app --host 0.0.0.0 --port 8000
"""
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import mongo
from app.core.exceptions import register_exception_handlers
from app.core.logging_config import configure_logging
from app.core.middleware import RequestContextMiddleware
from app.core.rate_limiter import RateLimitMiddleware
from app.core.redis_client import close_redis
from app.ml.model_loader import warm_up_models
from app.websockets.connection_manager import connection_manager

configure_logging()
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s (env=%s)", settings.PROJECT_NAME, settings.ENVIRONMENT)
    await mongo.connect()
    await warm_up_models()
    listener_task = asyncio.create_task(connection_manager.start_redis_listener())

    yield

    listener_task.cancel()
    await mongo.disconnect()
    await close_redis()
    logger.info("Shutdown complete.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Production-grade AI-powered disaster relief coordination platform.",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan,
)

# --- DEBUG: confirm what origins were actually parsed from env ---
logger.info("CORS origins loaded: %r", settings.BACKEND_CORS_ORIGINS)

# --- Middleware stack ---
# NOTE: Starlette applies middleware in REVERSE order of registration
# (last added = outermost = runs first). CORSMiddleware must be added
# LAST so it wraps everything else and can respond to preflight OPTIONS
# requests before they hit rate limiting or context middleware.
app.add_middleware(RequestContextMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS] or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

if settings.ENABLE_PROMETHEUS:
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")