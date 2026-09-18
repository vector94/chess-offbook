import pytest

from offbook.core.pgn import replay_moves


def test_replay_moves():
    plies = replay_moves("1. e4 c5 2. Nf3 Nc6")

    assert [p.ply for p in plies] == [1, 2, 3, 4]
    assert [p.side_to_move for p in plies] == ["white", "black", "white", "black"]
    assert plies[0].fen_before == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert plies[0].san == "e4"
    assert plies[0].uci == "e2e4"


def test_replay_moves_empty_pgn():
    with pytest.raises(ValueError):
        replay_moves("")
