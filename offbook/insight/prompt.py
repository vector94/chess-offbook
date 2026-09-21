import hashlib
import json

from offbook.models import ExplainRequest


def build_cache_key(request: ExplainRequest) -> str:
    moves = sorted(request.book_moves, key=lambda m: m.uci)
    moves_json = json.dumps([m.model_dump() for m in moves], sort_keys=True)
    payload = f"{request.fen}|{request.played_san}|{moves_json}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_prompt(request: ExplainRequest) -> str:
    book_list = ", ".join(f"{m.san} (played in {m.share:.0%} of games)" for m in request.book_moves)
    if not book_list:
        book_list = "no book moves recorded"
    opening = request.opening_name or "an unnamed opening"
    return (
        "You are a chess coach explaining a single moment in a game to the player, in plain English.\n\n"
        f"Opening: {opening}\n"
        f"Position (FEN): {request.fen}\n"
        f"The player played: {request.played_san}\n"
        f"The book move(s) at this position were: {book_list}\n"
        f"The game result for the player: {request.game_result}\n\n"
        "In 2-4 sentences, explain why the book move(s) were preferred over the "
        "move actually played. Be concrete about the chess reasoning (e.g. center "
        "control, piece activity, king safety), not generic praise. Do not repeat "
        "the move list verbatim; write naturally, as if reviewing the game with the player."
    )
