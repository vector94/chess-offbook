import { describe, expect, it } from "vitest";
import { buildSquareStyles } from "../src/lib/squareStyles";

describe("buildSquareStyles", () => {
  it("returns an empty object when nothing is selected and there are no legal targets", () => {
    expect(buildSquareStyles(null, [])).toEqual({});
  });

  it("styles the selected square", () => {
    const styles = buildSquareStyles("e2", []);
    expect(Object.keys(styles)).toEqual(["e2"]);
  });

  it("styles every legal target square", () => {
    const styles = buildSquareStyles(null, ["e3", "e4"]);
    expect(Object.keys(styles).sort()).toEqual(["e3", "e4"]);
  });

  it("styles both the selected square and its legal targets together", () => {
    const styles = buildSquareStyles("e2", ["e3", "e4"]);
    expect(Object.keys(styles).sort()).toEqual(["e2", "e3", "e4"]);
  });
});
