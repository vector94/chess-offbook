# OffBook web

Review page: enter a Chess.com username to see the latest game on a board,
where it left opening theory, its mistakes and blunders, and AI explanations.
It only talks to the `api` service over REST.

## Run

    npm install
    cp .env.example .env   # edit if your api service isn't on localhost:8000
    npm run dev             # dev server
    npm run build            # production build

The `api` service must be running separately, see the root README.
