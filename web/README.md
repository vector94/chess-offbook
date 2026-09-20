# OffBook web

Report page: enter a Chess.com username, watch it analyze, see where you left
opening theory. Talks only to the `api` service over REST — no direct
database or Python package access.

## Run

    npm install
    cp .env.example .env   # edit if your api service isn't on localhost:8000
    npm run dev             # dev server
    npm run build            # production build

The `api` service must be running separately (see the repo root README /
docs/design.md) — this project only talks to it over HTTP.
