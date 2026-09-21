CREATE TABLE explanations (
    cache_key   text PRIMARY KEY,
    fen         text NOT NULL,
    played_san  text NOT NULL,
    explanation text NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);
