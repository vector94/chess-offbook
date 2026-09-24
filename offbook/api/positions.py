import logging

import chess
import httpx
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from offbook.config import load_api_config
from offbook.core.explorer import fetch_explorer, moves_with_share
from offbook.models import BookMove

router = APIRouter()
logger = logging.getLogger(__name__)


class PositionStats(BaseModel):
    total_games: int
    moves: list[BookMove]


@router.get("/api/explorer")
def get_position_stats(fen: str = Query(max_length=100)) -> PositionStats:
    try:
        chess.Board(fen)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid fen")

    try:
        response = fetch_explorer(fen, load_api_config())
    except httpx.HTTPError as error:
        logger.warning("lichess explorer call failed: %s", error)
        raise HTTPException(status_code=502, detail="opening explorer unavailable")

    return PositionStats(total_games=response.total_games(), moves=moves_with_share(response))
