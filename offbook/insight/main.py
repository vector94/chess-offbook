import httpx
from fastapi import FastAPI

from offbook.insight.config import load_insight_config
from offbook.insight.db import get_cached_explanation, store_explanation
from offbook.insight.ollama_client import generate
from offbook.insight.prompt import build_cache_key, build_prompt
from offbook.models import ExplainRequest, ExplainResponse

app = FastAPI(title="OffBook Insight")


@app.post("/explain")
def explain(request: ExplainRequest) -> ExplainResponse:
    config = load_insight_config()
    cache_key = build_cache_key(request)

    cached = get_cached_explanation(config.database_url, cache_key)
    if cached is not None:
        return ExplainResponse(explanation=cached, cached=True)

    explanation = generate(build_prompt(request), config)

    try:
        store_explanation(config.database_url, cache_key, request.fen, request.played_san, explanation)
    except Exception:
        pass  # the cache only saves time, so don't fail the request because of it

    return ExplainResponse(explanation=explanation, cached=False)


@app.get("/healthz")
def healthz() -> dict:
    config = load_insight_config()
    with httpx.Client(timeout=5.0) as client:
        client.get(f"{config.ollama_base_url}/api/tags").raise_for_status()
    return {"status": "ok"}
