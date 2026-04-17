import { useThemeStore } from "./themeStore";

const ORDER: Array<"system" | "light" | "dark"> = ["system", "light", "dark"];
const ICON: Record<string, string> = { system: "🖥️", light: "☀️", dark: "🌙" };
const LABEL: Record<string, string> = { system: "System", light: "Light", dark: "Dark" };

export function ThemeToggle() {
  const { preference, setPreference } = useThemeStore();
  const next = () => {
    const idx = ORDER.indexOf(preference);
    const nextPref = ORDER[(idx + 1) % ORDER.length];
    void setPreference(nextPref);
  };
  return (
    <button
      type="button"
      onClick={next}
      className="btn btn-outline-light btn-sm"
      aria-label={`Theme: ${LABEL[preference]}. Click to change.`}
      title={`Theme: ${LABEL[preference]}`}
    >
      <span aria-hidden>{ICON[preference]}</span>
      <span className="ms-1 d-none d-sm-inline">{LABEL[preference]}</span>
    </button>
  );
}
