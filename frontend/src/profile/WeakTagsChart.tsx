import type { WeakTag } from "../api/types";
import { describeTag } from "../glossary";

export function WeakTagsChart({ weakTags }: { weakTags: WeakTag[] }) {
  if (!weakTags.length) {
    return (
      <p className="text-muted text-center">
        No weak areas detected yet — solve a few more rated problems.
      </p>
    );
  }
  return (
    <ul className="list-unstyled mb-0">
      {weakTags.map((w) => (
        <li key={w.tag} className="mb-3" title={describeTag(w.tag)}>
          <div className="d-flex justify-content-between">
            <strong>{w.tag}</strong>
            <span className="text-muted small">{w.pct}% behind</span>
          </div>
          <div className="progress" role="progressbar" aria-valuenow={w.pct} aria-valuemin={0} aria-valuemax={100}>
            <div className="progress-bar bg-danger progress-bar-striped" style={{ width: `${w.pct}%` }}>
              {w.pct}%
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
}
