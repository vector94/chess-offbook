from offbook.config import load_api_config
from offbook.core.detector import select_book_moves
from offbook.models import ExplorerMove, ExplorerResponse


def explorer_response(*game_counts):
    moves = []
    for i, count in enumerate(game_counts):
        moves.append(ExplorerMove(san=f"m{i}", uci=f"u{i}", white=count, draws=0, black=0))
    return ExplorerResponse(moves=moves)


def test_select_book_moves_uses_the_min_share():
    config = load_api_config()
    config.book_min_share = 0.05
    config.book_top_n = 0

    book = select_book_moves(explorer_response(5, 4, 91), config)

    assert [m.uci for m in book] == ["u2", "u0"]


def test_select_book_moves_keeps_the_top_moves():
    config = load_api_config()
    config.book_min_share = 0.9
    config.book_top_n = 2

    book = select_book_moves(explorer_response(40, 30, 20, 10), config)

    assert [m.uci for m in book] == ["u0", "u1"]
