import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { patchSettings } from "../api/endpoints";
import { HandleValidator } from "../components/HandleValidator";
import { useToastStore } from "../toast/toastStore";

interface Props {
  currentHandle: string | null;
  onClose: () => void;
}

export function ChangeHandleModal({ currentHandle, onClose }: Props) {
  const [handle, setHandle] = useState(currentHandle ?? "");
  const [valid, setValid] = useState(false);
  const push = useToastStore((s) => s.push);
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (cf_handle: string) => patchSettings({ cf_handle }),
    onSuccess: () => {
      push("Codeforces handle updated.", "success");
      queryClient.invalidateQueries();
      onClose();
    },
    onError: () => push("Could not update handle.", "danger"),
  });

  return (
    <>
      <div className="modal-backdrop fade show" onClick={onClose} aria-hidden="true" />
      <div className="modal fade show d-block" tabIndex={-1} role="dialog" aria-modal="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Change Codeforces handle</h5>
              <button type="button" className="btn-close" onClick={onClose} aria-label="Close" />
            </div>
            <div className="modal-body">
              <HandleValidator
                value={handle}
                onChange={setHandle}
                onValidated={setValid}
                id="change-cf-handle"
              />
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-primary"
                disabled={!valid || mutation.isPending}
                onClick={() => mutation.mutate(handle.trim())}
              >
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
