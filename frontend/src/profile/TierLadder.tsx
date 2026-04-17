import type { TierDef } from "../api/types";

interface Props {
  tiers: TierDef[];
  currentFloor: number;
  nextTarget: number;
  maxRating: number;
}

function rankFor(tiers: TierDef[], rating: number): number {
  if (!tiers.length) return -1;
  let idx = 0;
  for (let i = 0; i < tiers.length; i++) {
    if (rating >= tiers[i].floor) idx = i;
  }
  return idx;
}

export function TierLadder({ tiers, currentFloor, nextTarget, maxRating }: Props) {
  if (!tiers.length) return null;
  const userRank = rankFor(tiers, maxRating || currentFloor);
  const targetRank = tiers.findIndex((t) => t.target === nextTarget);

  return (
    <section className="mb-4" aria-label="Tier ladder">
      <h4 className="text-center mb-1">Tier ladder</h4>
      <p className="text-muted text-center small mb-3">
        Max rating <strong>{maxRating || "—"}</strong> — next milestone{" "}
        <strong>{nextTarget}</strong>
      </p>

      <div className="d-flex align-items-stretch overflow-auto gap-2 pb-2">
        {tiers.map((tier, i) => {
          const isCurrent = i === userRank;
          const isTarget = i === targetRank;
          const isPast = i < userRank;
          const baseClasses =
            "flex-shrink-0 text-center px-3 py-2 rounded border";
          const stateClasses = isCurrent
            ? "bg-primary text-white border-primary"
            : isTarget
              ? "bg-warning-subtle border-warning text-warning-emphasis"
              : isPast
                ? "bg-success-subtle border-success text-success-emphasis"
                : "bg-body-tertiary border-secondary-subtle text-muted";
          return (
            <div
              key={tier.key}
              className={`${baseClasses} ${stateClasses}`}
              style={{ minWidth: 120 }}
              aria-current={isCurrent ? "step" : undefined}
              title={`${tier.label}: ${tier.floor}–${tier.target - 1}`}
            >
              <div className="small fw-semibold text-truncate">{tier.label}</div>
              <div className="small opacity-75">
                {tier.floor}–{tier.target - 1}
              </div>
              {isCurrent && <div className="mt-1">📍 You</div>}
              {isTarget && !isCurrent && <div className="mt-1">🎯 Goal</div>}
              {isPast && <div className="mt-1">✓</div>}
            </div>
          );
        })}
      </div>
    </section>
  );
}
