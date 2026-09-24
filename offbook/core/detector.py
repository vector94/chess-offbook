from offbook.config import ApiConfig
from offbook.core.explorer import fetch_explorer, moves_with_share
from offbook.core.pgn import replay_moves
from offbook.models import BookMove, Deviation, ExplorerResponse, RawGame


def select_book_moves(response: ExplorerResponse, config: ApiConfig) -> list[BookMove]:
    # keep the top few moves, and any other move that is played often enough
    moves = moves_with_share(response)
    return [m for i, m in enumerate(moves) if i < config.book_top_n or m.share >= config.book_min_share]


def find_deviation(game: RawGame, config: ApiConfig) -> Deviation | None:
    for ply in replay_moves(game.pgn):
        if ply.side_to_move != game.color:
            continue
        if ply.ply > config.max_book_ply:
            return None

        response = fetch_explorer(ply.fen_before, config)
        if response.total_games() < config.book_min_games:
            return None

        book = select_book_moves(response, config)
        if any(m.uci == ply.uci for m in book):
            continue

        return Deviation(ply=ply.ply, book_moves=book)

    return None
