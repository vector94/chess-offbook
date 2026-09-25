# OffBook web

The React app for OffBook. It only talks to the `api` service.

## Run

```
npm install
cp .env.example .env
npm run dev
```

Change `VITE_API_BASE_URL` in `.env` if the api is not on `localhost:8000`.

To make a production build, run `npm run build`.

The `api` service must be running, see the main README.
