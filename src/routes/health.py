from fastapi import APIRouter

from src.config import settings
from src.config.expose import available_backends

health_router = APIRouter()


@health_router.get("/health")
async def health_check():
    """Health check endpoint for the gateway"""
    return dict(
        status="healthy",
        backends=available_backends,
        supported_methods=settings.ALLOWED_METHODS
    )
