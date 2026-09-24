import logging

import chess.engine
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from offbook.core.engine import find_mistakes
from offbook.models import FlaggedMove

router = APIRouter()
logger = logging.getLogger(__name__)

ENGINE_DEPTH = 14


class GameAnalysisRequest(BaseModel):
    pgn: str = Field(max_length=20000)


class GameAnalysisResponse(BaseModel):
    moves: list[FlaggedMove]


@router.post("/api/latest-game/analysis")
def analyze_game(request: GameAnalysisRequest) -> GameAnalysisResponse:
    try:
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        try:
            moves = find_mistakes(request.pgn, engine, ENGINE_DEPTH)
        finally:
            engine.quit()
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid pgn")
    except (OSError, chess.engine.EngineError) as error:
        logger.warning("engine analysis failed: %s", error)
        raise HTTPException(status_code=503, detail="engine analysis unavailable")

    return GameAnalysisResponse(moves=moves)
