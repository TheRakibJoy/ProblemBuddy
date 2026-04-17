import { create } from "zustand";
import { patchSettings } from "../api/endpoints";
import type { Theme } from "../api/types";

interface ThemeState {
  preference: Theme;
  effective: "light" | "dark";
  authed: boolean;
  setPreference: (pref: Theme) => Promise<void>;
  _applyEffective: () => void;
}

const mediaQuery = typeof window !== "undefined" ? window.matchMedia("(prefers-color-scheme: dark)") : null;

function computeEffective(pref: Theme): "light" | "dark" {
  if (pref === "system") return mediaQuery?.matches ? "dark" : "light";
  return pref;
}

function persistLocal(pref: Theme) {
  try {
    window.localStorage.setItem("pb_theme", pref);
  } catch {
    /* ignore */
  }
}

export function readLocal(): Theme {
  try {
    const raw = window.localStorage.getItem("pb_theme");
    if (raw === "system" || raw === "light" || raw === "dark") return raw;
  } catch {
    /* ignore */
  }
  return "system";
}

export const useThemeStore = create<ThemeState>((set, get) => ({
  preference: "system",
  effective: "light",
  authed: false,
  async setPreference(pref) {
    set({ preference: pref, effective: computeEffective(pref) });
    get()._applyEffective();
    if (get().authed) {
      try {
        await patchSettings({ theme_preference: pref });
      } catch {
        /* toast handled elsewhere */
      }
    } else {
      persistLocal(pref);
    }
  },
  _applyEffective() {
    const { effective } = get();
    document.documentElement.setAttribute("data-bs-theme", effective);
  },
}));

export function initTheme({ preference, authed }: { preference: Theme; authed: boolean }) {
  const effective = computeEffective(preference);
  useThemeStore.setState({ preference, effective, authed });
  useThemeStore.getState()._applyEffective();
  mediaQuery?.addEventListener("change", () => {
    if (useThemeStore.getState().preference === "system") {
      useThemeStore.setState({ effective: computeEffective("system") });
      useThemeStore.getState()._applyEffective();
    }
  });
}
