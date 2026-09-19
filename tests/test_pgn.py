import pytest

from offbook.core.pgn import position_key, replay_moves

SICILIAN_PGN = """
[Event "?"]

1. e4 c5 2. Nf3 Nc6
"""


def test_position_key_drops_halfmove_and_fullmove_counters():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    assert position_key(fen) == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"


def test_replay_moves_returns_one_entry_per_ply():
    plies = replay_moves(SICILIAN_PGN)

    assert [p.ply for p in plies] == [1, 2, 3, 4]


def test_replay_moves_first_ply_is_white_from_the_starting_position():
    plies = replay_moves(SICILIAN_PGN)

    first = plies[0]
    assert first.side_to_move == "white"
    assert first.fen_before == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert first.san == "e4"
    assert first.uci == "e2e4"


def test_replay_moves_alternates_side_to_move():
    plies = replay_moves(SICILIAN_PGN)

    assert [p.side_to_move for p in plies] == ["white", "black", "white", "black"]


def test_replay_moves_second_ply_reflects_the_first_move():
    plies = replay_moves(SICILIAN_PGN)

    second = plies[1]
    assert second.fen_before == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    assert second.san == "c5"


def test_replay_moves_raises_on_pgn_with_no_game():
    with pytest.raises(ValueError):
        replay_moves("")
