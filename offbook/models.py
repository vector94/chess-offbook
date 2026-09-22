from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class RawGame(BaseModel):
    chesscom_id: str
    played_at: datetime
    color: Literal["white", "black"]
    result: Literal["win", "draw", "loss"]
    pgn: str
    opening_name: str | None = None


class ExplorerMove(BaseModel):
    san: str
    uci: str
    white: int
    draws: int
    black: int


class ExplorerResponse(BaseModel):
    moves: list[ExplorerMove]
    white: int = 0
    draws: int = 0
    black: int = 0


class BookMove(BaseModel):
    san: str
    uci: str
    games: int
    share: float  # share of all games in this position, 0 to 1


class Deviation(BaseModel):
    ply: int
    book_moves: list[BookMove]


class ExplainRequest(BaseModel):
    fen: str
    played_san: str
    book_moves: list[BookMove]
    opening_name: str | None
    game_result: str


class ExplainResponse(BaseModel):
    explanation: str
    cached: bool
