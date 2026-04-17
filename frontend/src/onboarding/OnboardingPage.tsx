import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { patchSettings } from "../api/endpoints";
import { HandleValidator } from "../components/HandleValidator";
import { useToastStore } from "../toast/toastStore";

export function OnboardingPage() {
  const [handle, setHandle] = useState("");
  const [valid, setValid] = useState(false);
  const push = useToastStore((s) => s.push);

  const mutation = useMutation({
    mutationFn: (cf_handle: string) => patchSettings({ cf_handle }),
    onSuccess: () => {
      push("Linked your Codeforces handle.", "success");
      window.location.href = "/recommender/";
    },
    onError: () => push("Could not save your handle. Try again.", "danger"),
  });

  return (
    <div className="row justify-content-center">
      <div className="col-md-6">
        <div className="card shadow-sm">
          <div className="card-body">
            <h3 className="card-title text-center mb-3">Link your Codeforces account</h3>
            <p className="text-muted text-center">
              We use your Codeforces handle to read your solved problems and find your weak
              topics. This is different from your ProblemBuddy username.
            </p>
            <HandleValidator
              value={handle}
              onChange={setHandle}
              onValidated={setValid}
              label="Your Codeforces handle"
              id="onboarding-handle"
            />
            <button
              type="button"
              className="btn btn-primary w-100"
              disabled={!valid || mutation.isPending}
              onClick={() => mutation.mutate(handle.trim())}
            >
              {mutation.isPending ? "Saving…" : "Continue"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
