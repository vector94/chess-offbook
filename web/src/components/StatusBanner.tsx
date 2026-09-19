import type { GameStatus } from "../types";

interface StatusBannerProps {
  status: GameStatus;
}

const MESSAGES: Partial<Record<GameStatus, string>> = {
  check: "Check!",
  checkmate: "Checkmate",
  stalemate: "Stalemate",
  draw: "Draw",
};

export function StatusBanner({ status }: StatusBannerProps) {
  const message = MESSAGES[status];
  if (!message) return null;
  return <div className="status-banner">{message}</div>;
}
