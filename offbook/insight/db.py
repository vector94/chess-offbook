from pathlib import Path

import psycopg

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def run_migrations(database_url: str) -> None:
    with psycopg.connect(database_url, autocommit=True) as conn:
        for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            conn.execute(migration_file.read_text())


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
