import type { TierDef } from "../api/types";

interface Props {
  tiers: TierDef[];
  currentFloor: number;
  nextTarget: number;
  maxRating: number;
}

export function TierLadder({ tiers, currentFloor, nextTarget, maxRating }: Props) {
  if (!tiers.length) return null;
  const min = tiers[0].floor;
  const max = tiers[tiers.length - 1].target;
  const span = max - min || 1;
  const pct = (value: number) => `${Math.max(0, Math.min(100, ((value - min) / span) * 100))}%`;

  return (
    <div className="mb-4">
      <h4 className="text-center mb-3">Tier ladder</h4>
      <div className="position-relative" style={{ height: 80 }}>
        <div
          className="position-absolute top-50 start-0 end-0 translate-middle-y"
          style={{ height: 4, background: "var(--bs-border-color)" }}
        />
        {tiers.map((t) => (
          <div
            key={t.key}
            className="position-absolute top-50 translate-middle text-center"
            style={{ left: pct(t.floor) }}
          >
            <div
              className="rounded-circle bg-primary"
              style={{ width: 10, height: 10, margin: "0 auto" }}
              aria-hidden
            />
            <small className="d-block mt-1 text-muted" style={{ fontSize: "0.7em" }}>
              {t.label}
              <br />
              {t.floor}
            </small>
          </div>
        ))}
        <div
          className="position-absolute top-50 translate-middle"
          style={{ left: pct(maxRating || currentFloor) }}
          aria-label={`You are at rating ${maxRating || currentFloor}`}
        >
          <div
            style={{ fontSize: 28, lineHeight: 1, transform: "translateY(-60%)" }}
            aria-hidden
          >
            📍
          </div>
        </div>
      </div>
      <p className="text-muted text-center mt-3">
        Next milestone: <strong>{nextTarget}</strong>
      </p>
    </div>
  );
}
