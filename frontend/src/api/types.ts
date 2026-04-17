export interface Problem {
  id: number;
  pid: number;
  index: string;
  rating: number | null;
  tags: string[];
  matched_tags: string[];
  reason: string | null;
  url: string;
}

export interface RecommendResponse {
  problems: Problem[];
  generated_at: string;
  tier: string;
  next_target: number;
}

export interface WeakTag {
  tag: string;
  pct: number;
}

export interface TierDef {
  floor: number;
  target: number;
  key: string;
  label: string;
}

export interface ProfileSummary {
  username: string;
  email: string;
  cf_handle: string | null;
  max_rating: number;
  max_rank: string;
  photo: string | null;
  tier: string;
  current_floor: number;
  next_target: number;
  weak_tags: WeakTag[];
  tiers: TierDef[];
}

export type Theme = "system" | "light" | "dark";

export interface SettingsPayload {
  username: string;
  email: string;
  cf_handle: string | null;
  theme_preference: Theme;
  difficulty_offset: number;
  recommendations_per_load: number;
}

export interface HandleCheckResponse {
  handle: string;
  exists: boolean;
}

export type InteractionStatus = "solved" | "not_interested" | "hidden";

export interface TrainEnqueueResponse {
  task_id: string | null;
  handle: string;
  sync?: boolean;
}

export interface TrainStatusResponse {
  task_id: string;
  state: string;
  info: { tier?: string; done?: number; total?: number } | null;
  ready: boolean;
  successful: boolean | null;
}
