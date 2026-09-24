import logging

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from offbook.config import load_api_config
from offbook.core.chesscom import USERNAME_PATTERN, PlayerNotFound, fetch_recent_games
from offbook.core.detector import find_deviation
from offbook.models import BookMove

router = APIRouter()
logger = logging.getLogger(__name__)


class LatestGameResponse(BaseModel):
    found: bool
    chesscom_id: str | None = None
    pgn: str | None = None
    opening_name: str | None = None
    played_at: str | None = None
    game_result: str | None = None
    deviation_ply: int | None = None
    book_moves: list[BookMove] | None = None


@router.get("/api/latest-game")
def get_latest_game(username: str) -> LatestGameResponse:
    if not USERNAME_PATTERN.match(username):
        raise HTTPException(status_code=400, detail=f"invalid username: {username}")

    config = load_api_config()
    try:
        games = fetch_recent_games(username, config.chesscom_base_url)
        if not games:
            return LatestGameResponse(found=False)

        game = max(games, key=lambda g: g.played_at)
        deviation = find_deviation(game, config)
    except PlayerNotFound:
        raise HTTPException(status_code=404, detail=f"no such player: {username}")
    except httpx.HTTPError as error:
        logger.warning("latest game lookup failed: %s", error)
        raise HTTPException(status_code=502, detail="chess.com or lichess unavailable")

    return LatestGameResponse(
        found=True,
        chesscom_id=game.chesscom_id,
        pgn=game.pgn,
        opening_name=game.opening_name,
        played_at=game.played_at.isoformat(),
        game_result=game.result,
        deviation_ply=deviation.ply if deviation else None,
        book_moves=deviation.book_moves if deviation else None,
    )
