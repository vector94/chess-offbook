import logging

import httpx
from fastapi import HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def call_service(url: str, request: BaseModel, timeout: float) -> dict:
    """Sends the request to the insight service and returns its JSON answer."""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=request.model_dump())
        response.raise_for_status()
    except httpx.HTTPError as error:
        logger.warning("call to %s failed: %s", url, error)
        raise HTTPException(status_code=502, detail="service unavailable")

    return response.json()
