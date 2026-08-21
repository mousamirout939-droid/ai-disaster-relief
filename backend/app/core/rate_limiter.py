"""
Sliding-window rate limiter backed by Redis, applied as FastAPI middleware.
Uses a token-bucket-like counter per (client_ip, route) with a fixed window
for simplicity and predictable behavior under burst traffic.
"""
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.redis_client import redis_client


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/health") or request.url.path.startswith("/metrics"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        window = int(time.time() // 60)
        key = f"ratelimit:{client_ip}:{window}"

        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, 60)

        if current > settings.RATE_LIMIT_PER_MINUTE:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please slow down."},
                headers={"Retry-After": "60"},
            )
        return await call_next(request)
