import { describe, expect, it } from "vitest";
import { tagAccent } from "../tagAccent";

describe("tagAccent", () => {
  it("returns a stable gradient for the same tags", () => {
    expect(tagAccent(["dp", "math"])).toBe(tagAccent(["dp", "math"]));
  });

  it("returns a different gradient when tags change", () => {
    expect(tagAccent(["dp"])).not.toBe(tagAccent(["graphs"]));
  });

  it("falls back to neutral gradient when empty", () => {
    expect(tagAccent([])).toContain("linear-gradient");
  });
});
