from fastapi import APIRouter

from src.config import settings

health_router = APIRouter()


@health_router.get("/health")
async def health_check():
    """Health check endpoint for the gateway"""
    return dict(
        status="healthy",
        backends=settings.BACKENDS,
        supported_methods=settings.ALLOWED_METHODS
    )
