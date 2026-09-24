import time

import httpx

from offbook.config import USER_AGENT, ApiConfig
from offbook.models import BookMove, ExplorerResponse

RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

# Lichess writes castling as the king taking its own rook, python-chess uses e1g1 and so on
CASTLING_UCI = {"e1h1": "e1g1", "e1a1": "e1c1", "e8h8": "e8g8", "e8a8": "e8c8"}


def fetch_explorer(fen: str, config: ApiConfig) -> ExplorerResponse:
    headers = {"User-Agent": USER_AGENT}
    if config.lichess_token:
        headers["Authorization"] = f"Bearer {config.lichess_token}"

    url = f"{config.lichess_explorer_url}/lichess"
    params = {
        "fen": fen,
        "topGames": 0,
        "recentGames": 0,
        "speeds": ",".join(config.explorer_speeds),
        "ratings": ",".join(config.explorer_ratings),
    }

    with httpx.Client(headers=headers, timeout=10.0) as client:
        response = client.get(url, params=params)
        attempt = 1
        while response.status_code in RETRY_STATUS_CODES and attempt < config.http_retry_max:
            time.sleep(0.5 * 2 ** (attempt - 1))
            response = client.get(url, params=params)
            attempt += 1
    response.raise_for_status()

    result = ExplorerResponse.model_validate(response.json())
    for move in result.moves:
        move.uci = CASTLING_UCI.get(move.uci, move.uci)
    return result


def moves_with_share(response: ExplorerResponse) -> list[BookMove]:
    # the most played move comes first
    total = response.total_games()

    moves = []
    for move in response.moves:
        share = move.games / total if total > 0 else 0.0
        moves.append(BookMove(san=move.san, uci=move.uci, games=move.games, share=share))
    moves.sort(key=lambda m: m.games, reverse=True)

    return moves
