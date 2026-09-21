import type { LatestGame } from "./models";

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

export function getLatestGame(username: string): Promise<LatestGame> {
  return getJson(`/api/latest-game?username=${encodeURIComponent(username)}`);
}
