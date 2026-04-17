import "./styles.css";
import { initTheme, readLocal } from "./theme/themeStore";
import { mountIslands } from "./islands";
import type { Theme } from "./api/types";

interface BootData {
  authed: boolean;
  theme_preference: Theme;
}

function readBootData(): BootData {
  const node = document.getElementById("pb-boot-data");
  if (!node?.textContent) return { authed: false, theme_preference: readLocal() };
  try {
    return JSON.parse(node.textContent) as BootData;
  } catch {
    return { authed: false, theme_preference: readLocal() };
  }
}

try {
  console.info("[ProblemBuddy] main.tsx loaded");
  const boot = readBootData();
  initTheme({
    preference: boot.authed ? boot.theme_preference : readLocal(),
    authed: boot.authed,
  });
  mountIslands();
  console.info("[ProblemBuddy] islands mounted");
} catch (err) {
  console.error("[ProblemBuddy] bootstrap failed", err);
}
