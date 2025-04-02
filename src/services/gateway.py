from typing import Optional
from urllib.parse import urljoin

import httpx
from config import settings, http_client
from config.logs import logger
from fastapi import HTTPException, Request, status
from fastapi.responses import StreamingResponse


async def forward_request(
        request: Request,
        target_url: str,
        path: str,
        timeout: Optional[float] = settings.TIMEOUT_SECONDS
) -> StreamingResponse:
    """
    Forwards the incoming request to the target backend service.

    Args:
        request: The incoming FastAPI request
        target_url: Base URL of the target service
        path: The path portion of the URL to forward
        timeout: Request timeout in seconds
    """
    # Construct the full URL for the backend service
    url = urljoin(target_url, path)

    # Get the request body if present
    body = await request.body()

    # Forward all headers except host
    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        # Forward the request to the backend service
        response = await http_client.request(
            method=request.method,
            url=url,
            headers=headers,
            params=request.query_params,
            content=body,
            timeout=timeout
        )

        # Return the response as a streaming response
        return StreamingResponse(
            response.iter_bytes(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Gateway Timeout"
        )
    except httpx.RequestError:
        logger.exception('Request Failed')
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Bad Gateway"
        )
    except Exception as e:
        logger.exception('Request Failed')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )
