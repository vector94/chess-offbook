import logging
import queue
from contextlib import asynccontextmanager

import chess.engine
from fastapi import FastAPI, HTTPException

from offbook.engine.analysis import find_mistakes
from offbook.engine.config import load_engine_config
from offbook.engine.pool import EnginePool
from offbook.models import GameAnalysisRequest, GameAnalysisResponse

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start Stockfish here, so a wrong STOCKFISH_PATH fails at startup and not on the first request
    config = load_engine_config()
    app.state.config = config
    app.state.pool = EnginePool(config.stockfish_path, config.workers)
    yield
    app.state.pool.close()


app = FastAPI(title="OffBook Engine", lifespan=lifespan)


@app.post("/analyze")
def analyze(request: GameAnalysisRequest) -> GameAnalysisResponse:
    config = app.state.config
    pool = app.state.pool

    try:
        with pool.borrow(config.busy_timeout_seconds) as engine:
            moves = find_mistakes(request.pgn, engine, config.depth)
    except queue.Empty:
        raise HTTPException(status_code=503, detail="engine busy")
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid pgn")
    except chess.engine.EngineError as error:
        logger.warning("engine analysis failed: %s", error)
        raise HTTPException(status_code=503, detail="engine unavailable")

    return GameAnalysisResponse(moves=moves)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
