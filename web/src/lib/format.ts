export function moveLabel(ply: number, san: string): string {
  const moveNumber = Math.ceil(ply / 2);
  return ply % 2 === 1 ? `${moveNumber}. ${san}` : `${moveNumber}... ${san}`;
}

export function formatShare(share: number): string {
  const percent = share * 100;
  if (percent > 0 && percent < 1) return "<1%";

  return `${Math.round(percent)}%`;
}
