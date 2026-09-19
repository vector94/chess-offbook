# OffBook web

Standalone opening-practice board. Talks only to Lichess's Explorer API —
no dependency on the `offbook` backend.

## Run

npm install

Lichess now requires an API token for Explorer requests (since March 2026).
Get a free, **zero-scope** personal access token at
https://lichess.org/account/oauth/token (leave every scope checkbox
unchecked — it doesn't need access to your games, profile, or account,
only to identify the requester to Lichess for rate-limiting). Then:

    cp .env.example .env
    # edit .env and set VITE_LICHESS_TOKEN=<your token>

This is for personal/local use only. `VITE_LICHESS_TOKEN` is baked into
the client-side JS bundle at build time — anyone who opens this app's
network requests or reads its bundled source can see the token. Do not
deploy this app publicly with a real token still embedded in `.env`.

npm run dev      # dev server
npm test         # unit tests (pure logic only, see docs/superpowers/specs/2026-09-19-3d-opening-practice-board-design.md)
npm run build    # production build
