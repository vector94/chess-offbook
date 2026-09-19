import type { ExplorerMove, ExplorerResult, RawExplorerResponse } from "../types";

const EXPLORER_URL = "https://explorer.lichess.ovh/lichess";
const SPEEDS = "blitz,rapid,classical";
const RATINGS = "1600,1800,2000,2200";

export function parseExplorerResponse(raw: RawExplorerResponse): ExplorerResult {
  const moves: ExplorerMove[] = raw.moves
    .map((move) => {
      const games = move.white + move.draws + move.black;
      return {
        uci: move.uci,
        san: move.san,
        games,
        whiteWinPct: games === 0 ? 0 : (move.white / games) * 100,
        drawPct: games === 0 ? 0 : (move.draws / games) * 100,
        blackWinPct: games === 0 ? 0 : (move.black / games) * 100,
      };
    })
    .sort((a, b) => b.games - a.games);

  return {
    totalGames: raw.white + raw.draws + raw.black,
    moves,
    opening: raw.opening,
  };
}

export async function fetchExplorer(fen: string): Promise<ExplorerResult> {
  const url = `${EXPLORER_URL}?fen=${encodeURIComponent(fen)}&speeds=${SPEEDS}&ratings=${RATINGS}&topGames=0&recentGames=0`;
  const token: string | undefined = import.meta.env.VITE_LICHESS_TOKEN;
  const headers: HeadersInit | undefined = token ? { Authorization: `Bearer ${token}` } : undefined;
  const response = await fetch(url, { headers });
  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Lichess Explorer requires an API token — see web/README.md");
    }
    throw new Error(`explorer request failed: ${response.status}`);
  }
  const raw = (await response.json()) as RawExplorerResponse;
  return parseExplorerResponse(raw);
}
