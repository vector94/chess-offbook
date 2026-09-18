from offbook.config import ApiConfig
from offbook.core.explorer import fetch_explorer
from offbook.core.pgn import replay_moves
from offbook.models import BookMove, Deviation, ExplorerResponse, RawGame


def total_games(response: ExplorerResponse) -> int:
    # moves only has the most common moves, so use the top-level counts when we have them
    total = response.white + response.draws + response.black
    if total > 0:
        return total
    return sum(m.white + m.draws + m.black for m in response.moves)


def select_book_moves(response: ExplorerResponse, config: ApiConfig) -> list[BookMove]:
    total = total_games(response)

    moves = []
    for move in response.moves:
        games = move.white + move.draws + move.black
        share = games / total if total > 0 else 0.0
        moves.append(BookMove(san=move.san, uci=move.uci, games=games, share=share))
    moves.sort(key=lambda m: m.games, reverse=True)

    return [m for i, m in enumerate(moves) if i < config.book_top_n or m.share >= config.book_min_share]


def find_deviation(game: RawGame, config: ApiConfig) -> Deviation | None:
    for ply in replay_moves(game.pgn):
        if ply.side_to_move != game.color:
            continue
        if ply.ply > config.max_book_ply:
            return None

        response = fetch_explorer(ply.fen_before, config)
        if total_games(response) < config.book_min_games:
            return None

        book = select_book_moves(response, config)
        if any(m.uci == ply.uci for m in book):
            continue

        return Deviation(ply=ply.ply, book_moves=book)

    return None
