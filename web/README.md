# OffBook web

Review page: enter a Chess.com username to see the latest game on a board,
where it left opening theory, its mistakes and blunders, and AI explanations.
Talks only to the `api` service over REST — no direct database or Python
package access.

## Run

    npm install
    cp .env.example .env   # edit if your api service isn't on localhost:8000
    npm run dev             # dev server
    npm run build            # production build

The `api` service must be running separately (see the repo root README) —
this project only talks to it over HTTP.
