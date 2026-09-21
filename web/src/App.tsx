import { type SubmitEvent, useState } from "react";
import "./App.css";
import { GameReview } from "./components/GameReview";
import { getLatestGame } from "./lib/api";
import type { LatestGame } from "./lib/models";

type LatestGameState =
  | { phase: "loading" }
  | { phase: "error"; message: string }
  | { phase: "done"; data: LatestGame };

export function App() {
  const [username, setUsername] = useState("");
  // null until the first search
  const [latestGame, setLatestGame] = useState<LatestGameState | null>(null);

  async function checkLatestGame(event: SubmitEvent) {
    event.preventDefault();
    const name = username.trim();
    if (!name) return;

    setLatestGame({ phase: "loading" });
    try {
      setLatestGame({ phase: "done", data: await getLatestGame(name) });
    } catch (error) {
      setLatestGame({ phase: "error", message: (error as Error).message });
    }
  }

  return (
    <div>
      <h1>OffBook</h1>
      <form onSubmit={checkLatestGame}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Chess.com username"
        />
        <button type="submit" disabled={latestGame?.phase === "loading"}>
          Check latest game
        </button>
      </form>

      {latestGame?.phase === "loading" && <p>Loading...</p>}
      {latestGame?.phase === "error" && <p className="error">Error: {latestGame.message}</p>}
      {latestGame?.phase === "done" && !latestGame.data.found && <p>No games in the last two months.</p>}
      {latestGame?.phase === "done" && latestGame.data.found && <GameReview game={latestGame.data} />}
    </div>
  );
}
