import type { Color, FlaggedMove } from "./models";

export const ANNOTATION = { mistake: "?", blunder: "??" } as const;

export function moveLabel(ply: number, san: string): string {
  const moveNumber = Math.ceil(ply / 2);
  return ply % 2 === 1 ? `${moveNumber}. ${san}` : `${moveNumber}... ${san}`;
}

function plural(count: number, word: string): string {
  return `${count} ${word}${count === 1 ? "" : "s"}`;
}

export function summarizeMistakes(flagged: FlaggedMove[], color: Color): string {
  const own = flagged.filter((move) => move.color === color);
  if (own.length === 0) return "none";

  const mistakes = own.filter((move) => move.classification === "mistake").length;
  return `${plural(mistakes, "mistake")}, ${plural(own.length - mistakes, "blunder")}`;
}

export function formatShare(share: number): string {
  const percent = share * 100;
  if (percent > 0 && percent < 1) return "<1%";

  return `${Math.round(percent)}%`;
}
