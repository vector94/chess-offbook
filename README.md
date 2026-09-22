# OffBook

See where a player leaves chess opening theory.

## Running locally

Before starting the services:

- Postgres must be running locally, with an empty `offbook_insight_dev` database created:
  `psql -h localhost -c "CREATE DATABASE offbook_insight_dev"`. The `insight` service runs its
  own migrations on startup, so no manual migration step is needed once the empty database exists.
- Ollama must be running locally with the `llama3.1:8b` model pulled.

Then, in separate terminals:

```
uv run uvicorn offbook.api.main:app --port 8000
uv run uvicorn offbook.insight.main:app --port 8002
cd web && npm run dev
```
