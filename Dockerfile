# Shared by api, engine and insight. docker-compose.yml sets which one each container runs.
FROM python:3.12-slim

# Stockfish for the engine. Debian installs it outside the PATH.
RUN apt-get update \
    && apt-get install -y --no-install-recommends stockfish \
    && rm -rf /var/lib/apt/lists/*
ENV STOCKFISH_PATH=/usr/games/stockfish

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY offbook ./offbook
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
