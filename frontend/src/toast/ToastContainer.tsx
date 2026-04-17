import { useToastStore } from "./toastStore";

export function ToastContainer() {
  const { toasts, dismiss } = useToastStore();
  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      className="toast-container position-fixed bottom-0 end-0 p-3"
      style={{ zIndex: 1080 }}
    >
      {toasts.map((t) => (
        <div
          key={t.id}
          role="alert"
          className={`toast align-items-center text-bg-${t.kind} border-0 show mb-2`}
        >
          <div className="d-flex">
            <div className="toast-body">{t.message}</div>
            <button
              type="button"
              className="btn-close btn-close-white me-2 m-auto"
              aria-label="Close"
              onClick={() => dismiss(t.id)}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
