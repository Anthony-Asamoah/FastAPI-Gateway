import asyncio
import json
from typing import Dict, Optional, Any

from config import api_registry
from config.logs import logger
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, AnyUrl

from src.config import settings

services_router = APIRouter()


@services_router.get("")
async def show_services() -> Dict[str, str]:
    return api_registry


class RegisterServiceSchema(BaseModel):
    service_name: str
    service_url: AnyUrl


@services_router.post("/register")
async def register_service(payload: RegisterServiceSchema) -> Optional[Dict[str, Any]]:
    # check for existing name
    if api_registry.get(payload.service_name, None): raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"The name '{payload.service_name}' is already taken."
    )
    api_registry[payload.service_name] = str(payload.service_url)

    # log service to a file as persistence mechanism
    asyncio.create_task(write_service_to_file())
    return {"message": f"Service {payload.service_name} registered at {payload.service_url}"}


async def write_service_to_file() -> None:
    with open(settings.REG_FILE_NAME, 'w') as registry:
        registry.write(json.dumps(api_registry))
