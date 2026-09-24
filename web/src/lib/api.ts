import type { Deviation, LatestGame, PositionStats } from "./models";

const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail ?? `request failed: ${response.status}`);
  }

  return response.json();
}

async function getJson<T>(path: string): Promise<T> {
  return readJson<T>(await fetch(API_BASE_URL + path));
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(API_BASE_URL + path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  return readJson<T>(response);
}

export function getLatestGame(username: string): Promise<LatestGame> {
  return getJson(`/api/latest-game?username=${encodeURIComponent(username)}`);
}

export function getPositionStats(fen: string): Promise<PositionStats> {
  return getJson(`/api/explorer?fen=${encodeURIComponent(fen)}`);
}

export async function explainDeviation(deviation: Deviation): Promise<string> {
  const body = await postJson<{ explanation: string }>("/api/latest-game/explain", deviation);
  return body.explanation;
}
