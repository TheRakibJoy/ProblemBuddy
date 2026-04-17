import { useEffect, useState } from "react";
import { checkCfHandle } from "../api/endpoints";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onValidated: (valid: boolean) => void;
  label?: string;
  id?: string;
}

type Status = "idle" | "checking" | "valid" | "invalid" | "error";

export function HandleValidator({ value, onChange, onValidated, label = "Codeforces handle", id = "cf-handle" }: Props) {
  const [status, setStatus] = useState<Status>("idle");

  useEffect(() => {
    const trimmed = value.trim();
    if (!trimmed) {
      setStatus("idle");
      onValidated(false);
      return;
    }
    setStatus("checking");
    const handle = setTimeout(() => {
      checkCfHandle(trimmed)
        .then((res) => {
          if (res.exists) {
            setStatus("valid");
            onValidated(true);
          } else {
            setStatus("invalid");
            onValidated(false);
          }
        })
        .catch(() => {
          setStatus("error");
          onValidated(false);
        });
    }, 400);
    return () => clearTimeout(handle);
  }, [value, onValidated]);

  const message = {
    idle: "",
    checking: "Checking…",
    valid: "✓ Handle found on Codeforces",
    invalid: "✗ Handle not found",
    error: "Could not reach Codeforces",
  }[status];

  const messageClass = {
    idle: "text-muted",
    checking: "text-muted",
    valid: "text-success",
    invalid: "text-danger",
    error: "text-warning",
  }[status];

  return (
    <div className="mb-3">
      <label htmlFor={id} className="form-label">
        {label}
      </label>
      <input
        id={id}
        type="text"
        className="form-control"
        value={value}
        autoComplete="username"
        onChange={(e) => onChange(e.target.value)}
      />
      {message && <div className={`form-text ${messageClass}`}>{message}</div>}
    </div>
  );
}
