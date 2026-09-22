import httpx
from fastapi import APIRouter

from offbook.config import load_api_config
from offbook.models import ExplainRequest, ExplainResponse

router = APIRouter()

INSIGHT_TIMEOUT_SECONDS = 95.0  # a bit longer than insight's own 90s timeout for Ollama


@router.post("/api/latest-game/explain")
def explain_deviation(request: ExplainRequest) -> ExplainResponse:
    url = load_api_config().insight_service_url + "/explain"
    with httpx.Client(timeout=INSIGHT_TIMEOUT_SECONDS) as client:
        response = client.post(url, json=request.model_dump())
    response.raise_for_status()
    return ExplainResponse(**response.json())
