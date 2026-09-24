import queue

import chess.engine
import pytest

from offbook.engine.pool import EnginePool


class FakeEngine:
    def quit(self):
        pass


@pytest.fixture
def pool(monkeypatch):
    monkeypatch.setattr(chess.engine.SimpleEngine, "popen_uci", lambda path: FakeEngine())
    return EnginePool("stockfish", size=1)


def test_engine_goes_back_after_use(pool):
    with pool.borrow(timeout=1) as engine:
        pass

    with pool.borrow(timeout=1) as again:
        assert again is engine


def test_engine_goes_back_after_a_bad_pgn(pool):
    with pytest.raises(ValueError):
        with pool.borrow(timeout=1) as engine:
            raise ValueError("invalid PGN")

    with pool.borrow(timeout=1) as again:
        assert again is engine


def test_crashed_engine_is_replaced(pool):
    with pytest.raises(chess.engine.EngineError):
        with pool.borrow(timeout=1) as engine:
            raise chess.engine.EngineTerminatedError("stockfish crashed")

    with pool.borrow(timeout=1) as again:
        assert again is not engine


def test_busy_pool_raises_empty(pool):
    with pool.borrow(timeout=1):
        with pytest.raises(queue.Empty):
            with pool.borrow(timeout=0.01):
                pass
