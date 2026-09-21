import { Chess } from "chess.js";

export type ReplayMove = {
  ply: number;
  san: string;
  color: "w" | "b";
  fenBefore: string;
  fenAfter: string;
};

export function replayPgn(pgn: string): ReplayMove[] {
  const chess = new Chess();
  chess.loadPgn(pgn);

  return chess.history({ verbose: true }).map((move, index) => ({
    ply: index + 1,
    san: move.san,
    color: move.color,
    fenBefore: move.before,
    fenAfter: move.after,
  }));
}
