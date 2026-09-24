from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from offbook.api import explanations, latest_game, positions
from offbook.core.chesscom import PlayerNotFound, Profile, fetch_profile

app = FastAPI(title="OffBook API", version="0.1.0")
app.include_router(latest_game.router)
app.include_router(positions.router)
app.include_router(explanations.router)

# no cookies or auth, so "*" is fine
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

INDEX_FILE = Path(__file__).parent / "index.html"


@app.get("/")
def index() -> FileResponse:
    return FileResponse(INDEX_FILE)


@app.get("/api/profile")
def get_profile(username: str) -> Profile:
    try:
        return fetch_profile(username)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except PlayerNotFound:
        raise HTTPException(status_code=404, detail=f"no such player: {username}")


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
