from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field


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

    @property
    def games(self) -> int:
        return self.white + self.draws + self.black


class ExplorerResponse(BaseModel):
    moves: list[ExplorerMove]
    white: int = 0
    draws: int = 0
    black: int = 0

    def total_games(self) -> int:
        # moves only has the most common moves, so use the top-level counts when we have them
        total = self.white + self.draws + self.black
        if total > 0:
            return total
        return sum(move.games for move in self.moves)


class BookMove(BaseModel):
    san: str
    uci: str
    games: int
    share: float  # share of all games in this position, 0 to 1


class Deviation(BaseModel):
    ply: int
    book_moves: list[BookMove]


class ExplainRequest(BaseModel):
    fen: str = Field(max_length=100)
    played_san: str = Field(max_length=10)
    book_moves: list[BookMove] = Field(max_length=20)
    opening_name: str | None = Field(default=None, max_length=200)
    game_result: Literal["win", "draw", "loss"]


class ExplainResponse(BaseModel):
    explanation: str
    cached: bool


class MistakeExplainRequest(BaseModel):
    color: Literal["white", "black"]
    fen_before: str = Field(max_length=100)
    played_san: str = Field(max_length=10)
    classification: Literal["mistake", "blunder"]
    best_san: str = Field(max_length=10)
    best_line: list[Annotated[str, Field(max_length=10)]] = Field(max_length=10)
    win_chance_before: float = Field(ge=0.0, le=1.0)
    win_chance_after: float = Field(ge=0.0, le=1.0)


class FlaggedMove(MistakeExplainRequest):
    ply: int
