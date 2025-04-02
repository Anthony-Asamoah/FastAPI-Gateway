from fastapi import APIRouter

from .gateway import gateway_router
from .health import health_router
from .services import services_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(services_router, prefix="/services", tags=["Services"])
router.include_router(gateway_router, prefix="/gateway", tags=["Gateway"])
