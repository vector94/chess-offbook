import re
from datetime import UTC, datetime

import httpx

from offbook.config import USER_AGENT
from offbook.models import RawGame

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,50}$")
DRAW_RESULTS = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}


class PlayerNotFound(Exception):
    pass


def normalize_result(result: str) -> str:
    if result == "win":
        return "win"
    if result in DRAW_RESULTS:
        return "draw"
    return "loss"


def opening_name_from_eco_url(eco_url: str | None) -> str | None:
    # eco is a URL like ".../openings/Italian-Game"; keep the last part
    if eco_url is None:
        return None
    return eco_url.rstrip("/").split("/")[-1].replace("-", " ")


def parse_game(raw: dict, username: str) -> RawGame | None:
    if raw["white"]["username"].lower() == username:
        color = "white"
    elif raw["black"]["username"].lower() == username:
        color = "black"
    else:
        return None

    return RawGame(
        chesscom_id=raw["url"],
        played_at=datetime.fromtimestamp(raw["end_time"], tz=UTC),
        color=color,
        result=normalize_result(raw[color]["result"]),
        opening_name=opening_name_from_eco_url(raw.get("eco")),
        pgn=raw["pgn"],
    )


def fetch_recent_games(username: str, base_url: str, months_back: int = 2) -> list[RawGame]:
    username = username.lower()

    games = []
    with httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=10.0) as client:
        archives_response = client.get(f"{base_url}/pub/player/{username}/games/archives")
        if archives_response.status_code == 404:
            raise PlayerNotFound(username)
        archives_response.raise_for_status()

        for archive_url in archives_response.json()["archives"][-months_back:]:
            month_response = client.get(archive_url)
            month_response.raise_for_status()
            for raw in month_response.json().get("games", []):
                if raw.get("rules") != "chess":
                    continue
                game = parse_game(raw, username)
                if game is not None:
                    games.append(game)
    return games
