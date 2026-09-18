import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

USER_AGENT = "OffBook/0.1 (PA2577 course project)"


@dataclass
class ApiConfig:
    chesscom_base_url: str
    lichess_explorer_url: str
    book_min_share: float
    book_top_n: int
    book_min_games: int
    max_book_ply: int
    explorer_speeds: list[str]
    explorer_ratings: list[str]
    http_retry_max: int
    lichess_token: str | None


def env_list(name: str, default: str) -> list[str]:
    return os.environ.get(name, default).split(",")


def load_api_config() -> ApiConfig:
    return ApiConfig(
        chesscom_base_url=os.environ.get("CHESSCOM_BASE_URL", "https://api.chess.com"),
        lichess_explorer_url=os.environ.get("LICHESS_EXPLORER_URL", "https://explorer.lichess.ovh"),
        book_min_share=float(os.environ.get("BOOK_MIN_SHARE", "0.05")),
        book_top_n=int(os.environ.get("BOOK_TOP_N", "3")),
        book_min_games=int(os.environ.get("BOOK_MIN_GAMES", "50")),
        max_book_ply=int(os.environ.get("MAX_BOOK_PLY", "20")),
        explorer_speeds=env_list("EXPLORER_SPEEDS", "blitz,rapid,classical"),
        explorer_ratings=env_list("EXPLORER_RATINGS", "1600,1800,2000,2200"),
        http_retry_max=int(os.environ.get("HTTP_RETRY_MAX", "4")),
        lichess_token=os.environ.get("LICHESS_TOKEN"),
    )
