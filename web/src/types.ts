export type PieceType = "p" | "n" | "b" | "r" | "q" | "k";
export type PieceColor = "w" | "b";

export type GameStatus = "playing" | "check" | "checkmate" | "stalemate" | "draw";

export interface RawExplorerMove {
  uci: string;
  san: string;
  white: number;
  draws: number;
  black: number;
}

export interface RawExplorerResponse {
  white: number;
  draws: number;
  black: number;
  moves: RawExplorerMove[];
  opening: { eco: string; name: string } | null;
}

export interface ExplorerMove {
  uci: string;
  san: string;
  games: number;
  whiteWinPct: number;
  drawPct: number;
  blackWinPct: number;
}

export interface ExplorerResult {
  totalGames: number;
  moves: ExplorerMove[];
  opening: { eco: string; name: string } | null;
}
