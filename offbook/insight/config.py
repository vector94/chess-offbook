import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")


@dataclass
class InsightConfig:
    database_url: str
    ollama_base_url: str
    ollama_model: str
    generate_timeout_seconds: float


def load_insight_config() -> InsightConfig:
    return InsightConfig(
        database_url=os.environ.get("INSIGHT_DATABASE_URL", "postgresql://localhost/offbook_insight_dev"),
        ollama_base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.environ.get("OLLAMA_MODEL", "llama3.1:8b"),
        generate_timeout_seconds=float(os.environ.get("INSIGHT_GENERATE_TIMEOUT_SECONDS", "90")),
    )
