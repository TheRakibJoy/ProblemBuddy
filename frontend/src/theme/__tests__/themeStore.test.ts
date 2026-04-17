import { describe, expect, it } from "vitest";
import { initTheme, useThemeStore } from "../themeStore";

describe("themeStore", () => {
  it("applies system preference by default", () => {
    initTheme({ preference: "system", authed: false });
    const { preference, effective } = useThemeStore.getState();
    expect(preference).toBe("system");
    expect(["light", "dark"]).toContain(effective);
  });

  it("applies dark when explicitly dark", () => {
    initTheme({ preference: "dark", authed: false });
    expect(useThemeStore.getState().effective).toBe("dark");
    expect(document.documentElement.getAttribute("data-bs-theme")).toBe("dark");
  });
});
