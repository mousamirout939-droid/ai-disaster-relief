"""Centralized exception handlers registered on the FastAPI app for consistent error responses."""
import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

logger = logging.getLogger("app.exceptions")


class DomainException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Validation error", "errors": exc.errors()},
        )

    @app.exception_handler(PyMongoError)
    async def mongo_exception_handler(request: Request, exc: PyMongoError):
        logger.exception("MongoDB error")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Database temporarily unavailable. Please try again."},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred."},
        )
