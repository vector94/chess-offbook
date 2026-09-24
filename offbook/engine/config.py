import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")


@dataclass
class EngineConfig:
    stockfish_path: str
    depth: int
    workers: int
    busy_timeout_seconds: float


def load_engine_config() -> EngineConfig:
    return EngineConfig(
        stockfish_path=os.environ.get("STOCKFISH_PATH", "stockfish"),
        depth=int(os.environ.get("ENGINE_DEPTH", "14")),
        workers=int(os.environ.get("ENGINE_WORKERS", "2")),
        busy_timeout_seconds=float(os.environ.get("ENGINE_BUSY_TIMEOUT_SECONDS", "30")),
    )
