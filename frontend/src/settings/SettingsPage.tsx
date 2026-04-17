import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import {
  deleteAccount,
  fetchSettings,
  patchSettings,
} from "../api/endpoints";
import type { SettingsPayload, Theme } from "../api/types";
import { HandleValidator } from "../components/HandleValidator";
import { useThemeStore } from "../theme/themeStore";
import { useToastStore } from "../toast/toastStore";

export function SettingsPage() {
  const push = useToastStore((s) => s.push);
  const setThemePref = useThemeStore((s) => s.setPreference);
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["settings"],
    queryFn: fetchSettings,
  });
  const [form, setForm] = useState<SettingsPayload | null>(null);
  const [handleValid, setHandleValid] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [confirmPassword, setConfirmPassword] = useState("");

  useEffect(() => {
    if (data) setForm(data);
  }, [data]);

  const save = useMutation({
    mutationFn: (patch: Partial<SettingsPayload>) => patchSettings(patch),
    onSuccess: (next) => {
      setForm(next);
      push("Settings saved.", "success");
      queryClient.invalidateQueries({ queryKey: ["settings"] });
      queryClient.invalidateQueries({ queryKey: ["profile-summary"] });
    },
    onError: (err: Error) => push(err.message || "Could not save.", "danger"),
  });

  const del = useMutation({
    mutationFn: (password: string) => deleteAccount(password),
    onSuccess: () => {
      push("Account deleted.", "info");
      window.location.href = "/";
    },
    onError: () => push("Password incorrect.", "danger"),
  });

  if (isLoading || !form) return <div className="skeleton" style={{ height: 400 }} />;

  const saveHandler =
    (patch: Partial<SettingsPayload>) =>
    () => save.mutate(patch);

  return (
    <div className="row justify-content-center">
      <div className="col-md-8">
        <h1 className="h3 mb-3">Settings</h1>

        <section className="card mb-3 shadow-sm">
          <div className="card-body">
            <h2 className="h5 mb-3">Profile</h2>
            <label className="form-label" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              className="form-control mb-2"
              value={form.email}
              autoComplete="email"
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              onBlur={() => save.mutate({ email: form.email })}
            />
            <HandleValidator
              value={form.cf_handle ?? ""}
              onChange={(v) => setForm({ ...form, cf_handle: v })}
              onValidated={setHandleValid}
              label="Codeforces handle"
              id="cf-handle"
            />
            <button
              className="btn btn-outline-primary btn-sm"
              disabled={!handleValid || save.isPending}
              onClick={saveHandler({ cf_handle: form.cf_handle })}
            >
              Save handle
            </button>
            <div className="mt-3">
              <a href="/password/change/" className="btn btn-link p-0">
                Change password →
              </a>
            </div>
          </div>
        </section>

        <section className="card mb-3 shadow-sm">
          <div className="card-body">
            <h2 className="h5 mb-3">Recommendations</h2>
            <label className="form-label" htmlFor="recs-per-load">
              Problems per load: {form.recommendations_per_load}
            </label>
            <input
              id="recs-per-load"
              type="range"
              className="form-range mb-3"
              min={1}
              max={12}
              value={form.recommendations_per_load}
              onChange={(e) =>
                setForm({ ...form, recommendations_per_load: Number(e.target.value) })
              }
              onMouseUp={saveHandler({
                recommendations_per_load: form.recommendations_per_load,
              })}
              onTouchEnd={saveHandler({
                recommendations_per_load: form.recommendations_per_load,
              })}
            />
            <label className="form-label" htmlFor="difficulty-offset">
              Difficulty offset: {form.difficulty_offset > 0 ? "+" : ""}
              {form.difficulty_offset}
            </label>
            <input
              id="difficulty-offset"
              type="range"
              className="form-range"
              min={-300}
              max={300}
              step={50}
              value={form.difficulty_offset}
              onChange={(e) =>
                setForm({ ...form, difficulty_offset: Number(e.target.value) })
              }
              onMouseUp={saveHandler({ difficulty_offset: form.difficulty_offset })}
              onTouchEnd={saveHandler({ difficulty_offset: form.difficulty_offset })}
            />
            <div className="form-text">
              Negative = easier than your rating, positive = harder.
            </div>
          </div>
        </section>

        <section className="card mb-3 shadow-sm">
          <div className="card-body">
            <h2 className="h5 mb-3">Appearance</h2>
            <fieldset>
              <legend className="form-label mb-2">Theme</legend>
              {(["system", "light", "dark"] as Theme[]).map((theme) => (
                <div key={theme} className="form-check form-check-inline">
                  <input
                    id={`theme-${theme}`}
                    className="form-check-input"
                    type="radio"
                    name="theme"
                    checked={form.theme_preference === theme}
                    onChange={() => {
                      setForm({ ...form, theme_preference: theme });
                      void setThemePref(theme);
                      save.mutate({ theme_preference: theme });
                    }}
                  />
                  <label className="form-check-label text-capitalize" htmlFor={`theme-${theme}`}>
                    {theme}
                  </label>
                </div>
              ))}
            </fieldset>
          </div>
        </section>

        <section className="card mb-3 border-danger shadow-sm">
          <div className="card-body">
            <h2 className="h5 text-danger mb-3">Danger zone</h2>
            {!showDelete ? (
              <button className="btn btn-outline-danger" onClick={() => setShowDelete(true)}>
                Delete my account
              </button>
            ) : (
              <div>
                <p className="mb-2">
                  This permanently removes your ProblemBuddy account. Enter your password to
                  confirm.
                </p>
                <input
                  type="password"
                  className="form-control mb-2"
                  value={confirmPassword}
                  autoComplete="current-password"
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Current password"
                />
                <div className="d-flex gap-2">
                  <button
                    className="btn btn-danger"
                    disabled={!confirmPassword || del.isPending}
                    onClick={() => del.mutate(confirmPassword)}
                  >
                    Delete permanently
                  </button>
                  <button className="btn btn-secondary" onClick={() => setShowDelete(false)}>
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
