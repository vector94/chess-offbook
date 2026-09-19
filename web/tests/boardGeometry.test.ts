import { describe, expect, it } from "vitest";
import { positionToSquare, squareToPosition } from "../src/lib/boardGeometry";

describe("squareToPosition", () => {
  it("places a1 at the near-left corner for white orientation", () => {
    expect(squareToPosition("a1", "white")).toEqual([-3.5, 0, 3.5]);
  });

  it("places h8 at the far-right corner for white orientation", () => {
    expect(squareToPosition("h8", "white")).toEqual([3.5, 0, -3.5]);
  });

  it("mirrors both axes for black orientation", () => {
    expect(squareToPosition("a1", "black")).toEqual([3.5, 0, -3.5]);
    expect(squareToPosition("h8", "black")).toEqual([-3.5, 0, 3.5]);
  });

  it("rejects an invalid square", () => {
    expect(() => squareToPosition("z9", "white")).toThrow("invalid square: z9");
  });
});

describe("positionToSquare", () => {
  it("round-trips every square for white orientation", () => {
    for (const file of "abcdefgh") {
      for (let rank = 1; rank <= 8; rank++) {
        const square = `${file}${rank}`;
        const [x, , z] = squareToPosition(square, "white");
        expect(positionToSquare(x, z, "white")).toBe(square);
      }
    }
  });

  it("round-trips every square for black orientation", () => {
    for (const file of "abcdefgh") {
      for (let rank = 1; rank <= 8; rank++) {
        const square = `${file}${rank}`;
        const [x, , z] = squareToPosition(square, "black");
        expect(positionToSquare(x, z, "black")).toBe(square);
      }
    }
  });
});
