export type Orientation = "white" | "black";

const FILES = ["a", "b", "c", "d", "e", "f", "g", "h"];

export function squareToPosition(square: string, orientation: Orientation): [number, number, number] {
  const file = FILES.indexOf(square[0]);
  const rank = Number(square[1]) - 1;
  if (file === -1 || Number.isNaN(rank) || rank < 0 || rank > 7) {
    throw new Error(`invalid square: ${square}`);
  }
  const x = orientation === "white" ? file - 3.5 : 3.5 - file;
  const z = orientation === "white" ? 3.5 - rank : rank - 3.5;
  return [x, 0, z];
}

export function positionToSquare(x: number, z: number, orientation: Orientation): string {
  const file = orientation === "white" ? Math.round(x + 3.5) : Math.round(3.5 - x);
  const rank = orientation === "white" ? Math.round(3.5 - z) : Math.round(z + 3.5);
  return `${FILES[file]}${rank + 1}`;
}
