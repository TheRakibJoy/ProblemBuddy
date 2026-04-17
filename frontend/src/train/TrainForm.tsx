import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { enqueueTrain, fetchTrainStatus } from "../api/endpoints";
import { HandleValidator } from "../components/HandleValidator";
import { useToastStore } from "../toast/toastStore";

export function TrainForm() {
  const push = useToastStore((s) => s.push);
  const [handle, setHandle] = useState("");
  const [valid, setValid] = useState(false);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [completed, setCompleted] = useState(false);

  const enqueue = useMutation({
    mutationFn: (h: string) => enqueueTrain(h),
    onSuccess: (data) => {
      if (data.sync) {
        push(`Trained synchronously for ${data.handle}.`, "success");
        setCompleted(true);
        return;
      }
      if (data.task_id) {
        setTaskId(data.task_id);
        push(`Training ${data.handle}…`, "info");
      }
    },
    onError: () => push("Could not enqueue training.", "danger"),
  });

  const status = useQuery({
    queryKey: ["train-status", taskId],
    queryFn: () => fetchTrainStatus(taskId!),
    enabled: !!taskId && !completed,
    refetchInterval: (q) => {
      const data = q.state.data;
      if (!data) return 2000;
      if (data.ready) {
        setCompleted(true);
        push(
          data.successful ? `Training complete for ${handle}.` : "Training failed.",
          data.successful ? "success" : "danger",
        );
        return false;
      }
      return 2000;
    },
  });

  const info = status.data?.info;
  const done = info?.done ?? 0;
  const total = info?.total ?? 9;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <div className="row justify-content-center">
      <div className="col-md-6">
        <div className="card shadow-sm">
          <div className="card-body">
            <h1 className="h4 card-title text-center">Train with an inspiring handle</h1>
            <p className="text-muted text-center">
              Ingest a strong Codeforces user's solved problems into the recommender.
            </p>
            <HandleValidator
              value={handle}
              onChange={setHandle}
              onValidated={setValid}
              id="train-handle"
            />
            <button
              type="button"
              className="btn btn-primary btn-lg w-100"
              disabled={!valid || enqueue.isPending || (!!taskId && !completed)}
              onClick={() => enqueue.mutate(handle.trim().toLowerCase())}
            >
              {enqueue.isPending || (!!taskId && !completed) ? "Training…" : "Submit"}
            </button>

            {(taskId && !completed) && (
              <div className="mt-3">
                <div className="progress" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
                  <div
                    className="progress-bar progress-bar-striped progress-bar-animated"
                    style={{ width: `${pct}%` }}
                  >
                    {info?.label ?? "Starting…"} ({done}/{total})
                  </div>
                </div>
              </div>
            )}

            {completed && (
              <div className="alert alert-success mt-3">
                Training finished. Head to the recommender to see fresher picks.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
