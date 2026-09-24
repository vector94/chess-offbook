import logging
import time
from pathlib import Path

import psycopg

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

logger = logging.getLogger(__name__)


def run_migrations(database_url: str) -> None:
    with psycopg.connect(database_url, autocommit=True) as conn:
        for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            conn.execute(migration_file.read_text())


def run_migrations_with_retry(database_url: str, attempts: int = 15, delay_seconds: float = 2.0) -> None:
    # Postgres can start after insight (for example in Docker), so wait for it
    for attempt in range(1, attempts + 1):
        try:
            run_migrations(database_url)
            return
        except psycopg.OperationalError:
            if attempt == attempts:
                raise
            logger.warning("Postgres not reachable (attempt %d of %d), retrying", attempt, attempts)
            time.sleep(delay_seconds)


def check_database(database_url: str) -> None:
    with psycopg.connect(database_url, connect_timeout=3) as conn:
        conn.execute("SELECT 1")


def get_cached_explanation(database_url: str, cache_key: str) -> str | None:
    with psycopg.connect(database_url) as conn:
        row = conn.execute("SELECT explanation FROM explanations WHERE cache_key = %s", (cache_key,)).fetchone()
    if row is None:
        return None
    return row[0]


def store_explanation(database_url: str, cache_key: str, fen: str, played_san: str, explanation: str) -> None:
    with psycopg.connect(database_url, autocommit=True) as conn:
        conn.execute(
            """
            INSERT INTO explanations (cache_key, fen, played_san, explanation)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (cache_key) DO NOTHING
            """,
            (cache_key, fen, played_san, explanation),
        )
