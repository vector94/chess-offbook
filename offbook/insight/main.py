import logging
from contextlib import asynccontextmanager

import httpx
import psycopg
from fastapi import FastAPI, HTTPException

from offbook.insight.config import load_insight_config
from offbook.insight.db import check_database, get_cached_explanation, run_migrations_with_retry, store_explanation
from offbook.insight.ollama_client import generate, model_is_pulled
from offbook.insight.prompt import build_mistake_prompt, build_prompt, cache_key
from offbook.logs import configure_logging
from offbook.models import ExplainRequest, ExplainResponse, MistakeExplainRequest

configure_logging()
logger = logging.getLogger(__name__)


def explain_with_cache(prompt: str, fen: str, played_san: str) -> ExplainResponse:
    config = load_insight_config()
    key = cache_key(prompt, config.ollama_model)

    # the cache only saves time, so if the database fails we still answer
    try:
        cached = get_cached_explanation(config.database_url, key)
    except Exception:
        logger.warning("failed to read cached explanation", exc_info=True)
        cached = None
    if cached is not None:
        return ExplainResponse(explanation=cached, cached=True)

    try:
        explanation = generate(prompt, config)
    except httpx.HTTPError as error:
        logger.warning("ollama call failed: %s", error)
        raise HTTPException(status_code=502, detail="language model unavailable")

    try:
        store_explanation(config.database_url, key, fen, played_san, explanation)
    except Exception:
        logger.warning("failed to cache explanation", exc_info=True)

    return ExplainResponse(explanation=explanation, cached=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations_with_retry(load_insight_config().database_url)
    yield


app = FastAPI(title="OffBook Insight", lifespan=lifespan)


@app.post("/explain")
def explain(request: ExplainRequest) -> ExplainResponse:
    return explain_with_cache(build_prompt(request), request.fen, request.played_san)


@app.post("/explain-mistake")
def explain_mistake(request: MistakeExplainRequest) -> ExplainResponse:
    return explain_with_cache(build_mistake_prompt(request), request.fen_before, request.played_san)


# healthz only says the process is up, readyz also checks Postgres, Ollama and the model
@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict:
    config = load_insight_config()
    down = []

    try:
        check_database(config.database_url)
    except psycopg.Error:
        down.append("database")

    try:
        if not model_is_pulled(config):
            down.append("model not pulled yet")
    except httpx.HTTPError:
        down.append("language model")

    if down:
        raise HTTPException(status_code=503, detail="not ready: " + ", ".join(down))
    return {"status": "ok"}
