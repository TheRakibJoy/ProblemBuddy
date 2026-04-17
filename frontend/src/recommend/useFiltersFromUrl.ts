import type { Filters } from "./FilterBar";

export function readFiltersFromUrl(defaults: Filters): Filters {
  const params = new URLSearchParams(window.location.search);
  const parseList = (key: string): string[] => {
    const raw = params.get(key);
    if (!raw) return defaults[key as keyof Filters] as string[];
    return raw
      .split(",")
      .map((t) => t.trim().toLowerCase())
      .filter(Boolean);
  };
  const parseInt = (key: string, fallback: number): number => {
    const raw = params.get(key);
    if (raw === null) return fallback;
    const n = Number(raw);
    return Number.isFinite(n) ? n : fallback;
  };
  return {
    tags: parseList("tags"),
    exclude_tags: parseList("exclude_tags"),
    min: parseInt("min", defaults.min),
    max: parseInt("max", defaults.max),
    weak_only: params.get("weak_only") === "1",
    count: parseInt("count", defaults.count),
  };
}
