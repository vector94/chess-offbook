import logging
import queue
from collections.abc import Iterator
from contextlib import contextmanager

import chess.engine

logger = logging.getLogger(__name__)


class EnginePool:
    """A fixed number of running Stockfish processes. The size is also the limit on parallel analyses."""

    def __init__(self, stockfish_path: str, size: int):
        self.stockfish_path = stockfish_path
        self.idle = queue.Queue()
        for _ in range(size):
            self.idle.put(chess.engine.SimpleEngine.popen_uci(stockfish_path))

    @contextmanager
    def borrow(self, timeout: float) -> Iterator[chess.engine.SimpleEngine]:
        """Lends out an idle engine and always takes it back. Raises queue.Empty if none is free in time."""
        engine = self.idle.get(timeout=timeout)
        try:
            yield engine
        except chess.engine.EngineError:
            # the engine broke, so a new one goes back into the pool in its place
            engine = self.restart(engine)
            raise
        finally:
            if engine is not None:
                self.idle.put(engine)

    def restart(self, engine: chess.engine.SimpleEngine) -> chess.engine.SimpleEngine | None:
        try:
            engine.quit()
        except Exception:
            pass
        try:
            return chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
        except (OSError, chess.engine.EngineError):
            logger.warning("could not restart a crashed engine, the pool is one engine smaller", exc_info=True)
            return None

    def close(self) -> None:
        while not self.idle.empty():
            engine = self.idle.get()
            try:
                engine.quit()
            except Exception:
                pass
