import logging

import httpx
from fastapi import HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def call_service(url: str, request: BaseModel, timeout: float) -> dict:
    """Sends the request to the engine or insight service and returns its JSON answer."""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=request.model_dump())
    except httpx.HTTPError as error:
        logger.warning("call to %s failed: %s", url, error)
        raise HTTPException(status_code=502, detail="service unavailable")

    # pass the error on with the same status, for example 400 for a bad PGN or 503 when the engine is busy
    if response.is_error:
        logger.warning("%s returned %d", url, response.status_code)
        raise HTTPException(status_code=response.status_code, detail="service error")

    return response.json()
