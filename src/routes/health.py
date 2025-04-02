import asyncio
from typing import Dict

import httpx
from config import settings
from fastapi import APIRouter

from src.config import api_registry

health_router = APIRouter()


@health_router.get("")
async def health_check():
    """Health check endpoint for the gateway"""

    status = dict(
        status="healthy",
        backends=api_registry.copy(),
        supported_methods=settings.ALLOWED_METHODS
    )

    async def check_backend(label: str, url: str) -> Dict[str, str]:
        """Check health of a single backend service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=1.0)
                response.raise_for_status()
                return {label: "healthy"}
        except Exception:
            return {label: "unhealthy"}

    # Create tasks for all backend health checks
    backend_checks = [
        check_backend(label, url)
        for label, url in api_registry.items()
    ]

    # Run all checks concurrently
    backend_results = await asyncio.gather(*backend_checks)

    # Update status dictionary with results
    for result in backend_results:
        for label, health in result.items():
            status["backends"][label] = health
            if health == "unhealthy":
                status["status"] = "unhealthy"

    return status
