from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from offbook.api import analysis, explanations, latest_game, positions

app = FastAPI(title="OffBook API")
app.include_router(latest_game.router)
app.include_router(positions.router)
app.include_router(analysis.router)
app.include_router(explanations.router)

# no cookies or auth, so "*" is fine
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
