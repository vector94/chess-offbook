from fastapi import APIRouter

from offbook.api.services import call_service
from offbook.config import load_api_config
from offbook.models import GameAnalysisRequest, GameAnalysisResponse

router = APIRouter()

ENGINE_TIMEOUT_SECONDS = 60.0  # the engine may wait 30s for a free Stockfish before it starts


@router.post("/api/latest-game/analysis")
def analyze_game(request: GameAnalysisRequest) -> GameAnalysisResponse:
    url = load_api_config().engine_service_url + "/analyze"
    return GameAnalysisResponse(**call_service(url, request, ENGINE_TIMEOUT_SECONDS))
