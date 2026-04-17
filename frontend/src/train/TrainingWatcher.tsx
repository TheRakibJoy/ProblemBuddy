import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useRef, useState } from "react";
import { fetchActiveTraining } from "../api/endpoints";
import type { TrainingJob } from "../api/types";
import { useToastStore } from "../toast/toastStore";

export function TrainingWatcher() {
  const push = useToastStore((s) => s.push);
  const queryClient = useQueryClient();
  const seenTerminal = useRef<number | null>(null);
  const [dismissed, setDismissed] = useState(false);

  const query = useQuery({
    queryKey: ["active-training"],
    queryFn: fetchActiveTraining,
    refetchInterval: (q) => {
      const job = q.state.data?.job;
      if (!job) return 15_000;
      if (job.status === "queued" || job.status === "running") return 2_500;
      return 15_000;
    },
  });

  const job: TrainingJob | null = query.data?.job ?? null;

  useEffect(() => {
    if (!job) return;
    if (job.status === "success" && seenTerminal.current !== job.id) {
      seenTerminal.current = job.id;
      push(`Training complete for ${job.handle}.`, "success");
      queryClient.invalidateQueries({ queryKey: ["recommend"] });
      queryClient.invalidateQueries({ queryKey: ["profile-summary"] });
    } else if (job.status === "failed" && seenTerminal.current !== job.id) {
      seenTerminal.current = job.id;
      push(`Training failed for ${job.handle}.`, "danger");
    }
  }, [job, push, queryClient]);

  useEffect(() => {
    // Re-enable the card if a newer job appears.
    if (job && job.status !== "success" && job.status !== "failed") {
      setDismissed(false);
    }
  }, [job?.id, job?.status]);

  if (!job || dismissed) return null;

  const pct = job.total > 0 ? Math.round((job.done / job.total) * 100) : 0;
  const finished = job.status === "success" || job.status === "failed";

  return (
    <div
      className="position-fixed shadow-lg"
      style={{ bottom: 16, right: 16, width: 320, zIndex: 1070 }}
      role="status"
      aria-live="polite"
    >
      <div className="card border-primary">
        <div className="card-body py-2 px-3">
          <div className="d-flex justify-content-between align-items-center mb-1">
            <strong className="small">
              {job.status === "success" && "✓ "}
              {job.status === "failed" && "✗ "}
              Training {job.handle}
            </strong>
            <button
              type="button"
              className="btn-close btn-close-sm"
              aria-label="Dismiss"
              onClick={() => setDismissed(true)}
            />
          </div>
          {!finished && (
            <>
              <div className="progress" style={{ height: 10 }}>
                <div
                  className="progress-bar progress-bar-striped progress-bar-animated"
                  style={{ width: `${pct}%` }}
                  role="progressbar"
                  aria-valuenow={pct}
                  aria-valuemin={0}
                  aria-valuemax={100}
                />
              </div>
              <div className="small text-muted mt-1">
                {job.current_tier || "Starting…"} ({job.done}/{job.total})
              </div>
            </>
          )}
          {job.status === "success" && (
            <div className="small text-success">All tiers ingested. New recommendations ready.</div>
          )}
          {job.status === "failed" && (
            <div className="small text-danger">
              Something went wrong. Check the server log.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
