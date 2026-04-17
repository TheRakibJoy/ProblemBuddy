import type { Problem, WeakTag } from "../api/types";

interface Props {
  problem: Problem | null;
  weakTags: WeakTag[];
  onClose: () => void;
}

export function ExplainDrawer({ problem, weakTags, onClose }: Props) {
  if (!problem) return null;
  const problemTags = new Set(problem.tags.map((t) => t.toLowerCase()));
  const relevant = weakTags.filter((w) => problemTags.has(w.tag.toLowerCase()));
  const other = weakTags.filter((w) => !problemTags.has(w.tag.toLowerCase())).slice(0, 5);

  return (
    <div className="offcanvas offcanvas-end show" tabIndex={-1} style={{ visibility: "visible" }}>
      <div className="offcanvas-header">
        <h5 className="offcanvas-title">
          Why problem {problem.pid}{problem.index}?
        </h5>
        <button type="button" className="btn-close" aria-label="Close" onClick={onClose}></button>
      </div>
      <div className="offcanvas-body">
        <p className="mb-2">
          This problem was ranked highly because its tags overlap with topics where you
          trail the reference cohort.
        </p>
        <h6 className="mt-3">Matching weak tags</h6>
        {relevant.length === 0 ? (
          <p className="text-muted small">None of your flagged weak tags match — it's a broad-fit pick.</p>
        ) : (
          <ul className="list-unstyled">
            {relevant.map((w) => (
              <li key={w.tag} className="mb-2">
                <div className="d-flex justify-content-between">
                  <span className="fw-semibold">{w.tag}</span>
                  <span className="text-muted small">{w.pct}% behind</span>
                </div>
                <div className="progress" role="progressbar" aria-valuenow={w.pct}>
                  <div className="progress-bar bg-danger" style={{ width: `${w.pct}%` }}></div>
                </div>
              </li>
            ))}
          </ul>
        )}
        {other.length > 0 && (
          <>
            <h6 className="mt-4">Your other gaps</h6>
            <ul className="list-unstyled small text-muted mb-0">
              {other.map((w) => (
                <li key={w.tag}>
                  {w.tag} — {w.pct}% behind
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
}
