import { describe, expect, it, beforeEach } from "vitest";
import { readFiltersFromUrl } from "../useFiltersFromUrl";
import type { Filters } from "../FilterBar";

const defaults: Filters = {
  tags: [],
  exclude_tags: [],
  min: 800,
  max: 3500,
  weak_only: false,
  count: 3,
};

describe("readFiltersFromUrl", () => {
  beforeEach(() => {
    window.history.replaceState(null, "", "/");
  });

  it("returns defaults when no query", () => {
    expect(readFiltersFromUrl(defaults)).toEqual(defaults);
  });

  it("parses tags and rating range", () => {
    window.history.replaceState(null, "", "/?tags=dp,math&min=1200&max=1800&weak_only=1&count=5");
    const filters = readFiltersFromUrl(defaults);
    expect(filters.tags).toEqual(["dp", "math"]);
    expect(filters.min).toBe(1200);
    expect(filters.max).toBe(1800);
    expect(filters.weak_only).toBe(true);
    expect(filters.count).toBe(5);
  });
});
