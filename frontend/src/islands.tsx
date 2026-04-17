import { ComponentType } from "react";
import { createRoot } from "react-dom/client";
import { AppProviders } from "./providers";
import { ThemeToggle } from "./theme/ThemeToggle";
import { RecommendPage } from "./recommend/RecommendPage";
import { OnboardingPage } from "./onboarding/OnboardingPage";
import { ProfilePage } from "./profile/ProfilePage";
import { SettingsPage } from "./settings/SettingsPage";
import { TrainForm } from "./train/TrainForm";
import { TrainingWatcher } from "./train/TrainingWatcher";

type IslandProps = Record<string, unknown>;

const ISLANDS: Record<string, ComponentType<IslandProps>> = {
  "theme-toggle": ThemeToggle as ComponentType<IslandProps>,
  recommend: RecommendPage as ComponentType<IslandProps>,
  onboarding: OnboardingPage as ComponentType<IslandProps>,
  profile: ProfilePage as ComponentType<IslandProps>,
  settings: SettingsPage as ComponentType<IslandProps>,
  train: TrainForm as ComponentType<IslandProps>,
  "training-watcher": TrainingWatcher as ComponentType<IslandProps>,
};

export function mountIslands() {
  for (const el of document.querySelectorAll<HTMLElement>("[data-react-island]")) {
    const name = el.dataset.reactIsland;
    if (!name) continue;
    const Component = ISLANDS[name];
    if (!Component) {
      console.warn(`Unknown island: ${name}`);
      continue;
    }
    let props: IslandProps = {};
    if (el.dataset.props) {
      try {
        props = JSON.parse(el.dataset.props);
      } catch (err) {
        console.error(`Invalid island props for ${name}`, err);
      }
    }
    const root = createRoot(el);
    root.render(
      <AppProviders>
        <Component {...props} />
      </AppProviders>,
    );
  }
}
