import { useState } from "react";
import type { Problem } from "../api/types";
import { tagAccent } from "./tagAccent";

interface Props {
  problem: Problem;
  onMarkSolved: (problem: Problem) => void;
  onNotInterested: (problem: Problem) => void;
  onExplain: (problem: Problem) => void;
}

export function ProblemCard({ problem, onMarkSolved, onNotInterested, onExplain }: Props) {
  const [removing, setRemoving] = useState(false);
  const accent = tagAccent(problem.tags);

  const handleRemove = (action: () => void) => {
    setRemoving(true);
    setTimeout(action, 180);
  };

  return (
    <div
      className={`card h-100 shadow-sm transition-opacity ${
        removing ? "opacity-0 -translate-y-2" : "opacity-100"
      }`}
      style={{ transition: "opacity 180ms ease, transform 180ms ease" }}
    >
      <div
        className="card-img-top d-flex align-items-center justify-content-center text-white fw-bold"
        style={{ background: accent, height: 80, fontSize: 18 }}
        aria-hidden="true"
      >
        {problem.pid}
        {problem.index}
      </div>
      <div className="card-body d-flex flex-column">
        <h5 className="card-title mb-1">
          Codeforces <span className="badge bg-primary">{problem.pid}{problem.index}</span>
        </h5>
        <p className="card-subtitle text-muted mb-2">
          Rating <span className="badge bg-danger">{problem.rating ?? "?"}</span>
        </p>
        <div className="mb-2 d-flex flex-wrap gap-1" aria-label="Tags">
          {problem.tags.map((tag) => (
            <span
              key={tag}
              className={`badge ${problem.matched_tags.includes(tag) ? "bg-warning text-dark" : "bg-secondary"}`}
            >
              {tag}
            </span>
          ))}
        </div>
        {problem.reason && (
          <button
            type="button"
            onClick={() => onExplain(problem)}
            className="btn btn-link btn-sm p-0 text-start mb-2"
            aria-label="Explain why this problem was picked"
          >
            {problem.reason}
          </button>
        )}
        <a
          href={problem.url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-primary mt-auto w-100"
        >
          Solve this
        </a>
        <div className="d-flex gap-2 mt-2">
          <button
            type="button"
            className="btn btn-outline-success btn-sm flex-fill"
            onClick={() => handleRemove(() => onMarkSolved(problem))}
            aria-label={`Mark ${problem.pid}${problem.index} as solved`}
          >
            ✅ Solved
          </button>
          <button
            type="button"
            className="btn btn-outline-secondary btn-sm flex-fill"
            onClick={() => handleRemove(() => onNotInterested(problem))}
            aria-label={`Skip ${problem.pid}${problem.index}`}
          >
            🚫 Skip
          </button>
        </div>
      </div>
    </div>
  );
}
