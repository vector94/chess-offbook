import chess
import pytest
from chess.engine import Cp, Mate, PovScore

from offbook.engine.analysis import analyse_game, classify


class FakeEngine:
    # scores is {ply: (score for White, best line in UCI)}, other plies are level
    def __init__(self, scores):
        self.scores = scores

    def analyse(self, board, limit, game=None):
        score, pv = self.scores.get(board.ply(), (Cp(0), []))
        return {"score": PovScore(score, chess.WHITE), "pv": [chess.Move.from_uci(uci) for uci in pv]}


def test_classify():
    assert classify(0.05) is None
    assert classify(0.10) == "mistake"
    assert classify(0.15) == "blunder"


def test_scholars_mate_blunder():
    engine = FakeEngine({5: (Cp(0), ["g7g6", "h5f3"]), 6: (Mate(1), ["h5f7"])})

    analysis = analyse_game("1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7#", engine, depth=14)
    moves = analysis.moves

    assert len(moves) == 1
    assert moves[0].played_san == "Nf6"
    assert moves[0].classification == "blunder"
    assert moves[0].best_san == "g6"

    # 7 moves give 8 positions, and White won in the last one
    assert len(analysis.white_win_chances) == 8
    assert analysis.white_win_chances[-1] == 1.0


def test_illegal_move():
    with pytest.raises(ValueError):
        analyse_game("1. e4 e5 2. Ke3", FakeEngine({}), depth=14)
