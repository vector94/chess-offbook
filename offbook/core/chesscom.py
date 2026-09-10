import re
from datetime import UTC, datetime

import httpx
from pydantic import BaseModel

CHESSCOM_BASE_URL = "https://api.chess.com"
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,50}$")
USER_AGENT = "OffBook/0.1 (PA2577 course project)"


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
