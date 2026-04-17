import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { ApiError } from "../api/client";
import { enqueueTrain } from "../api/endpoints";
import { HandleValidator } from "../components/HandleValidator";
import { useToastStore } from "../toast/toastStore";

export function TrainForm() {
  const push = useToastStore((s) => s.push);
  const queryClient = useQueryClient();
  const [handle, setHandle] = useState("");
  const [valid, setValid] = useState(false);

  const enqueue = useMutation({
    mutationFn: (h: string) => enqueueTrain(h),
    onSuccess: (job) => {
      push(
        `Training ${job.handle} started. Keep browsing — a progress card in the corner will track it.`,
        "info",
      );
      setHandle("");
      queryClient.invalidateQueries({ queryKey: ["active-training"] });
    },
    onError: (err: Error) => {
      if (err instanceof ApiError && err.status === 409) {
        push("A training is already in progress — it'll finish shortly.", "warning");
      } else {
        push("Could not start training. Try again.", "danger");
      }
    },
  });

  return (
    <div className="row justify-content-center">
      <div className="col-md-6">
        <div className="card shadow-sm">
          <div className="card-body">
            <h1 className="h4 card-title text-center">Train with an inspiring handle</h1>
            <p className="text-muted text-center">
              Submit a strong Codeforces handle to enrich the recommender. The job
              runs in the background — you can navigate freely and a progress card
              in the corner will keep you posted.
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
              disabled={!valid || enqueue.isPending}
              onClick={() => enqueue.mutate(handle.trim().toLowerCase())}
            >
              {enqueue.isPending ? "Starting…" : "Start training"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
