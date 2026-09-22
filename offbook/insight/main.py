import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from offbook.insight.config import load_insight_config
from offbook.insight.db import get_cached_explanation, run_migrations, store_explanation
from offbook.insight.ollama_client import generate
from offbook.insight.prompt import build_prompt, cache_key
from offbook.models import ExplainRequest, ExplainResponse

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations(load_insight_config().database_url)
    yield


app = FastAPI(title="OffBook Insight", lifespan=lifespan)


@app.post("/explain")
def explain(request: ExplainRequest) -> ExplainResponse:
    config = load_insight_config()
    prompt = build_prompt(request)
    key = cache_key(prompt)

    cached = get_cached_explanation(config.database_url, key)
    if cached is not None:
        return ExplainResponse(explanation=cached, cached=True)

    explanation = generate(prompt, config)

    try:
        store_explanation(config.database_url, key, request.fen, request.played_san, explanation)
    except Exception:
        logger.warning("failed to cache explanation", exc_info=True)

    return ExplainResponse(explanation=explanation, cached=False)


@app.get("/healthz")
def healthz() -> dict:
    config = load_insight_config()
    with httpx.Client(timeout=5.0) as client:
        client.get(f"{config.ollama_base_url}/api/tags").raise_for_status()
    return {"status": "ok"}
