from fastapi import APIRouter

from .gateway import gateway_router
from .health import health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(gateway_router)
