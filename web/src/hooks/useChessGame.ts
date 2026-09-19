import { useMemo, useState } from "react";
import { Chess } from "chess.js";
import type { Square } from "chess.js";
import type { GameStatus } from "../types";

export type Orientation = "white" | "black";

export interface UseChessGame {
  fen: string;
  selectedSquare: string | null;
  legalTargets: string[];
  status: GameStatus;
  orientation: Orientation;
  selectSquare: (square: string) => void;
  attemptMove: (from: string, to: string) => boolean;
  playMove: (uci: string) => void;
  reset: () => void;
  flipBoard: () => void;
}

function computeStatus(game: Chess): GameStatus {
  if (game.isCheckmate()) return "checkmate";
  if (game.isStalemate()) return "stalemate";
  if (game.isDraw()) return "draw";
  if (game.isCheck()) return "check";
  return "playing";
}

function isGameOver(status: GameStatus): boolean {
  return status === "checkmate" || status === "stalemate" || status === "draw";
}

export function useChessGame(): UseChessGame {
  const [game] = useState(() => new Chess());
  const [fen, setFen] = useState(game.fen());
  const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
  const [orientation, setOrientation] = useState<Orientation>("white");

  const status = useMemo(() => computeStatus(game), [game, fen]);

  const legalTargets = useMemo<string[]>(() => {
    if (!selectedSquare) return [];
    return game
      .moves({ square: selectedSquare as Square, verbose: true })
      .map((move) => move.to);
  }, [game, selectedSquare, fen]);

  function attemptMove(from: string, to: string): boolean {
    if (isGameOver(status)) return false;
    try {
      const move = game.move({ from, to, promotion: "q" });
      if (!move) return false;
      setFen(game.fen());
      setSelectedSquare(null);
      return true;
    } catch {
      return false;
    }
  }

  function selectSquare(square: string) {
    if (isGameOver(status)) return;

    if (selectedSquare && legalTargets.includes(square)) {
      attemptMove(selectedSquare, square);
      return;
    }

    const moves = game.moves({ square: square as Square, verbose: true });
    setSelectedSquare(moves.length > 0 ? square : null);
  }

  function playMove(uci: string) {
    const from = uci.slice(0, 2);
    const to = uci.slice(2, 4);
    attemptMove(from, to);
  }

  function reset() {
    game.reset();
    setFen(game.fen());
    setSelectedSquare(null);
  }

  function flipBoard() {
    setOrientation((current) => (current === "white" ? "black" : "white"));
  }

  return {
    fen,
    selectedSquare,
    legalTargets,
    status,
    orientation,
    selectSquare,
    attemptMove,
    playMove,
    reset,
    flipBoard,
  };
}
