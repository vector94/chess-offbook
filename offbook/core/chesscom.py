import re
from datetime import UTC, datetime

import httpx
from pydantic import BaseModel

from offbook.config import USER_AGENT
from offbook.models import RawGame

CHESSCOM_BASE_URL = "https://api.chess.com"
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,50}$")
DRAW_RESULTS = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}


class PlayerNotFound(Exception):
    pass


class Profile(BaseModel):
    username: str
    name: str | None
    avatar: str | None
    country: str | None
    followers: int
    url: str
    joined: datetime
    last_online: datetime
    ratings: dict[str, int]


def fetch_profile(username: str) -> Profile:
    if not USERNAME_PATTERN.match(username):
        raise ValueError(f"invalid username: {username}")

    handle = username.lower()
    base = CHESSCOM_BASE_URL
    headers = {"User-Agent": USER_AGENT}

    with httpx.Client(headers=headers, timeout=10.0) as client:
        profile_response = client.get(f"{base}/pub/player/{handle}")
        if profile_response.status_code == 404:
            raise PlayerNotFound(username)
        profile_response.raise_for_status()

        stats_response = client.get(f"{base}/pub/player/{handle}/stats")
        stats_response.raise_for_status()

    return build_profile(profile_response.json(), stats_response.json())


def read_rating(stats: dict, key: str) -> int | None:
    section = stats.get(key)
    if section is None:
        return None
    last = section.get("last")
    if last is None:
        return None
    return last.get("rating")


def build_profile(profile: dict, stats: dict) -> Profile:
    rating_keys = [
        ("chess_rapid", "rapid"),
        ("chess_blitz", "blitz"),
        ("chess_bullet", "bullet"),
        ("chess_daily", "daily"),
    ]
    ratings = {}
    for api_key, short_name in rating_keys:
        rating = read_rating(stats, api_key)
        if rating is not None:
            ratings[short_name] = rating

    # country is a URL like ".../pub/country/US"; keep the last part
    country_url = profile.get("country", "")
    country = country_url.split("/")[-1]
    if country == "":
        country = None

    return Profile(
        username=profile["username"],
        name=profile.get("name"),
        avatar=profile.get("avatar"),
        country=country,
        followers=profile.get("followers", 0),
        url=profile.get("url", ""),
        joined=datetime.fromtimestamp(profile["joined"], tz=UTC),
        last_online=datetime.fromtimestamp(profile["last_online"], tz=UTC),
        ratings=ratings,
    )


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
