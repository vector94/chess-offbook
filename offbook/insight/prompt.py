import hashlib

from offbook.models import ExplainRequest, MistakeExplainRequest


def cache_key(prompt: str) -> str:
    # the prompt holds everything that changes the answer, so a changed prompt gets a new key by itself
    return hashlib.sha256(prompt.encode()).hexdigest()


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


def build_mistake_prompt(request: MistakeExplainRequest) -> str:
    mover = request.color.capitalize()
    opponent = "Black" if request.color == "white" else "White"
    # name the side on every move, small models lose track of whose move it is
    sides = [mover, opponent]
    line = ", ".join(f"{sides[i % 2]} {san}" for i, san in enumerate(request.best_line))
    return (
        "You are a chess coach commenting on one move from a game, in plain English.\n\n"
        f"Position (FEN, before the move): {request.fen_before}\n"
        f"{mover} played: {request.played_san}\n"
        f"{mover}'s better move was {request.best_san}. Engine line: {line}\n"
        f"{mover}'s winning chances went from {request.win_chance_before:.0%} to "
        f"{request.win_chance_after:.0%}, so {request.played_san} was a {request.classification}.\n\n"
        f"In 2-4 sentences, explain why {request.played_san} was a {request.classification} and why "
        f"{request.best_san} is better. Use only the position and the moves given here; do not invent "
        "tactics or variations that are not in the engine line. Refer to the players as White and Black; "
        'never use "you", "we" or "our".'
    )
