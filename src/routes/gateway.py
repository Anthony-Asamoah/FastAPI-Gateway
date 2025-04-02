from config import settings
from fastapi import HTTPException, APIRouter, status
from services.gateway import forward_request
from starlette.requests import Request

from src.config import api_registry

gateway_router = APIRouter()


@gateway_router.api_route(
    "/{app_name}/{path:path}",
    methods=settings.ALLOWED_METHODS_LIST
)
async def gateway(app_name: str, path: str, request: Request):
    """
    Main gateway route that handles all incoming requests.

    Args:
        app_name: Name of the target application (app1, app2, app3)
        path: The remaining path to forward
        request: The incoming FastAPI request
    """
    # Check if the requested application exists
    if app_name not in api_registry: raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{app_name} was not found."
    )

    # Get the backend URL for the requested application
    backend_url = api_registry[app_name]

    # Forward the request and return the response
    return await forward_request(request, backend_url, path)
