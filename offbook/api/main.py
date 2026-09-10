from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from offbook.core.chesscom import PlayerNotFound, Profile, fetch_profile

app = FastAPI(title="OffBook API", version="0.1.0")

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
