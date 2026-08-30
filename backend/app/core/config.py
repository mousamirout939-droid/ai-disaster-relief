"""
Centralized application configuration.
All values are sourced from environment variables (12-factor app style),
with sane development defaults. Never hardcode secrets here.
"""
import json
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App metadata ---
    PROJECT_NAME: str = "AI Disaster Relief & Rescue Platform"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = Field(default="development")  # development | staging | production
    DEBUG: bool = False

    # --- Security / Auth ---
    SECRET_KEY: str = Field(..., description="JWT signing secret, min 32 chars")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30

    # --- CORS ---
    # Kept as a raw string (not list[str]) to avoid pydantic-settings'
    # built-in JSON parsing of list-typed env vars, which throws a
    # SettingsError before any custom validator gets a chance to run.
    # Accepts either a comma-separated string or a JSON array string.
    BACKEND_CORS_ORIGINS: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        raw = self.BACKEND_CORS_ORIGINS.strip()
        if not raw:
            return []
        if raw.startswith("["):
            return json.loads(raw)
        return [i.strip() for i in raw.split(",") if i.strip()]

    # --- MongoDB ---
    MONGODB_URI: str = Field(..., description="MongoDB Atlas connection string")
    MONGODB_DB_NAME: str = "disaster_relief_platform"
    MONGODB_MAX_POOL_SIZE: int = 100
    MONGODB_MIN_POOL_SIZE: int = 10

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_RATE_LIMIT_DB: int = 1
    REDIS_CACHE_TTL_SECONDS: int = 300

    # --- Rate limiting ---
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 20

    # --- File storage (S3-compatible) ---
    STORAGE_BACKEND: str = "s3"  # s3 | local
    S3_BUCKET_NAME: str = "disaster-relief-media"
    S3_REGION: str = "us-east-1"
    S3_ENDPOINT_URL: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    LOCAL_UPLOAD_DIR: str = "/data/uploads"
    MAX_UPLOAD_SIZE_MB: int = 15

    # --- AI / ML ---
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-pro"
    YOLO_WEIGHTS_PATH: str = "app/ml/weights/severity_yolov8.pt"
    YOLO_CONFIDENCE_THRESHOLD: float = 0.35
    ML_INFERENCE_DEVICE: str = "cpu"  # cpu | cuda

    # --- Notifications ---
    SMS_PROVIDER_SID: Optional[str] = None
    SMS_PROVIDER_TOKEN: Optional[str] = None
    PUSH_NOTIFICATION_KEY: Optional[str] = None
    ALERT_BROADCAST_RADIUS_KM: float = 25.0

    # --- Celery / async tasks ---
    CELERY_BROKER_URL: str = "redis://localhost:6379/2"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/3"

    # --- Observability ---
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str] = None
    ENABLE_PROMETHEUS: bool = True

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — avoids re-parsing env on every import."""
    return Settings()


settings = get_settings()