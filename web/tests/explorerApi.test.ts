import { describe, expect, it } from "vitest";
import { parseExplorerResponse } from "../src/lib/explorerApi";
import type { RawExplorerResponse } from "../src/types";

describe("parseExplorerResponse", () => {
  it("sorts moves by game count descending", () => {
    const raw: RawExplorerResponse = {
      white: 100,
      draws: 20,
      black: 80,
      opening: null,
      moves: [
        { uci: "e2e4", san: "e4", white: 30, draws: 5, black: 15 },
        { uci: "d2d4", san: "d4", white: 60, draws: 10, black: 50 },
      ],
    };

    const result = parseExplorerResponse(raw);

    expect(result.moves.map((m) => m.uci)).toEqual(["d2d4", "e2e4"]);
  });

  it("computes win/draw/loss percentages per move", () => {
    const raw: RawExplorerResponse = {
      white: 50,
      draws: 25,
      black: 25,
      opening: null,
      moves: [{ uci: "e2e4", san: "e4", white: 50, draws: 25, black: 25 }],
    };

    const [move] = parseExplorerResponse(raw).moves;

    expect(move.games).toBe(100);
    expect(move.whiteWinPct).toBe(50);
    expect(move.drawPct).toBe(25);
    expect(move.blackWinPct).toBe(25);
  });

  it("computes totalGames from the top-level counts, not the moves list", () => {
    const raw: RawExplorerResponse = {
      white: 10,
      draws: 2,
      black: 3,
      opening: null,
      moves: [],
    };

    expect(parseExplorerResponse(raw).totalGames).toBe(15);
  });

  it("handles an empty moves list without dividing by zero", () => {
    const raw: RawExplorerResponse = { white: 0, draws: 0, black: 0, opening: null, moves: [] };

    const result = parseExplorerResponse(raw);

    expect(result.moves).toEqual([]);
    expect(result.totalGames).toBe(0);
  });

  it("passes through the opening field", () => {
    const raw: RawExplorerResponse = {
      white: 1,
      draws: 0,
      black: 0,
      opening: { eco: "C50", name: "Italian Game" },
      moves: [],
    };

    expect(parseExplorerResponse(raw).opening).toEqual({ eco: "C50", name: "Italian Game" });
  });
});
