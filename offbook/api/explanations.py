from fastapi import APIRouter

from offbook.api.services import call_service
from offbook.config import load_api_config
from offbook.models import ExplainRequest, ExplainResponse, MistakeExplainRequest

router = APIRouter()

INSIGHT_TIMEOUT_SECONDS = 95.0  # a bit longer than insight's own 90s timeout for Ollama


@router.post("/api/latest-game/explain")
def explain_deviation(request: ExplainRequest) -> ExplainResponse:
    url = load_api_config().insight_service_url + "/explain"
    return ExplainResponse(**call_service(url, request, INSIGHT_TIMEOUT_SECONDS))


@router.post("/api/latest-game/explain-mistake")
def explain_mistake(request: MistakeExplainRequest) -> ExplainResponse:
    url = load_api_config().insight_service_url + "/explain-mistake"
    return ExplainResponse(**call_service(url, request, INSIGHT_TIMEOUT_SECONDS))
