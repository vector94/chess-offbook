from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from offbook.api import analysis, explanations, latest_game, positions
from offbook.config import load_api_config
from offbook.logs import configure_logging

configure_logging()

app = FastAPI(title="OffBook API")
app.include_router(latest_game.router)
app.include_router(positions.router)
app.include_router(analysis.router)
app.include_router(explanations.router)

# no cookies or auth, so "*" is fine locally; set CORS_ORIGINS to the web app's origin when deployed
app.add_middleware(
    CORSMiddleware, allow_origins=load_api_config().cors_origins, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
