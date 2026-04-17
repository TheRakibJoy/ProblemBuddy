import { useEffect, useState } from "react";

export interface Filters {
  tags: string[];
  exclude_tags: string[];
  min: number;
  max: number;
  weak_only: boolean;
  count: number;
}

interface Props {
  initial: Filters;
  onChange: (filters: Filters) => void;
}

export function FilterBar({ initial, onChange }: Props) {
  const [tagInput, setTagInput] = useState("");
  const [excludeInput, setExcludeInput] = useState("");
  const [filters, setFilters] = useState<Filters>(initial);

  useEffect(() => {
    onChange(filters);
    const params = new URLSearchParams(window.location.search);
    params.set("tags", filters.tags.join(","));
    params.set("exclude_tags", filters.exclude_tags.join(","));
    params.set("min", String(filters.min));
    params.set("max", String(filters.max));
    params.set("weak_only", filters.weak_only ? "1" : "0");
    params.set("count", String(filters.count));
    window.history.replaceState(null, "", `?${params.toString()}`);
  }, [filters, onChange]);

  const addTag = (list: "tags" | "exclude_tags", value: string, reset: () => void) => {
    const tag = value.trim().toLowerCase();
    if (!tag) return;
    setFilters((f) => ({ ...f, [list]: Array.from(new Set([...f[list], tag])) }));
    reset();
  };
  const removeTag = (list: "tags" | "exclude_tags", tag: string) =>
    setFilters((f) => ({ ...f, [list]: f[list].filter((t) => t !== tag) }));

  return (
    <section aria-label="Filters" className="card shadow-sm mb-3">
      <div className="card-body">
        <div className="row g-3">
          <div className="col-md-6">
            <label className="form-label" htmlFor="include-tag-input">Must include tags</label>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                addTag("tags", tagInput, () => setTagInput(""));
              }}
              className="d-flex gap-1"
            >
              <input
                id="include-tag-input"
                className="form-control form-control-sm"
                placeholder="e.g. dp"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
              />
              <button className="btn btn-primary btn-sm" type="submit">Add</button>
            </form>
            <div className="mt-2 d-flex flex-wrap gap-1">
              {filters.tags.map((t) => (
                <button
                  key={t}
                  type="button"
                  className="badge bg-primary border-0"
                  onClick={() => removeTag("tags", t)}
                  aria-label={`Remove include tag ${t}`}
                >
                  {t} ×
                </button>
              ))}
            </div>
          </div>

          <div className="col-md-6">
            <label className="form-label" htmlFor="exclude-tag-input">Exclude tags</label>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                addTag("exclude_tags", excludeInput, () => setExcludeInput(""));
              }}
              className="d-flex gap-1"
            >
              <input
                id="exclude-tag-input"
                className="form-control form-control-sm"
                placeholder="e.g. brute force"
                value={excludeInput}
                onChange={(e) => setExcludeInput(e.target.value)}
              />
              <button className="btn btn-outline-secondary btn-sm" type="submit">Add</button>
            </form>
            <div className="mt-2 d-flex flex-wrap gap-1">
              {filters.exclude_tags.map((t) => (
                <button
                  key={t}
                  type="button"
                  className="badge bg-secondary border-0"
                  onClick={() => removeTag("exclude_tags", t)}
                  aria-label={`Remove exclude tag ${t}`}
                >
                  {t} ×
                </button>
              ))}
            </div>
          </div>

          <div className="col-md-4">
            <label className="form-label" htmlFor="min-rating">Min rating: {filters.min}</label>
            <input
              id="min-rating"
              type="range"
              min={800}
              max={3500}
              step={100}
              className="form-range"
              value={filters.min}
              onChange={(e) => setFilters((f) => ({ ...f, min: Number(e.target.value) }))}
            />
          </div>
          <div className="col-md-4">
            <label className="form-label" htmlFor="max-rating">Max rating: {filters.max}</label>
            <input
              id="max-rating"
              type="range"
              min={800}
              max={3500}
              step={100}
              className="form-range"
              value={filters.max}
              onChange={(e) => setFilters((f) => ({ ...f, max: Number(e.target.value) }))}
            />
          </div>
          <div className="col-md-2">
            <label className="form-label" htmlFor="count">Per load</label>
            <input
              id="count"
              type="number"
              min={1}
              max={12}
              className="form-control form-control-sm"
              value={filters.count}
              onChange={(e) => setFilters((f) => ({ ...f, count: Number(e.target.value) }))}
            />
          </div>
          <div className="col-md-2 d-flex align-items-end">
            <div className="form-check form-switch">
              <input
                id="weak-only"
                className="form-check-input"
                type="checkbox"
                checked={filters.weak_only}
                onChange={(e) => setFilters((f) => ({ ...f, weak_only: e.target.checked }))}
              />
              <label className="form-check-label" htmlFor="weak-only">
                Weak tags only
              </label>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
