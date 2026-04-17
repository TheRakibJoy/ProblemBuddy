import { apiFetch } from "./client";
import type {
  HandleCheckResponse,
  InteractionStatus,
  ProfileSummary,
  RecommendResponse,
  SettingsPayload,
  TrainingJob,
} from "./types";

export interface RecommendFilters {
  count?: number;
  tags?: string[];
  exclude_tags?: string[];
  min?: number;
  max?: number;
  weak_only?: boolean;
}

export function fetchRecommendations(filters: RecommendFilters = {}) {
  return apiFetch<RecommendResponse>("/api/recommend/", {
    params: {
      count: filters.count,
      tags: filters.tags?.join(",") || undefined,
      exclude_tags: filters.exclude_tags?.join(",") || undefined,
      min: filters.min,
      max: filters.max,
      weak_only: filters.weak_only ? "1" : undefined,
    },
  });
}

export function postInteraction(problem_id: number, status: InteractionStatus) {
  return apiFetch<void>("/api/interactions/", {
    method: "POST",
    body: { problem_id, status },
  });
}

export function fetchProfileSummary() {
  return apiFetch<ProfileSummary>("/api/profile/summary/");
}

export function checkCfHandle(handle: string) {
  return apiFetch<HandleCheckResponse>("/api/cf/handle-check/", {
    params: { handle },
  });
}

export function fetchSettings() {
  return apiFetch<SettingsPayload>("/api/settings/");
}

export function patchSettings(payload: Partial<SettingsPayload>) {
  return apiFetch<SettingsPayload>("/api/settings/", {
    method: "PATCH",
    body: payload,
  });
}

export function deleteAccount(password: string) {
  return apiFetch<void>("/api/account/delete/", {
    method: "POST",
    body: { password },
  });
}

export function enqueueTrain(handle: string) {
  return apiFetch<TrainingJob>("/api/train/", {
    method: "POST",
    body: { handle },
  });
}

export function fetchTrainStatus(jobId: number) {
  return apiFetch<TrainingJob>(`/api/train/${jobId}/`);
}

export function fetchActiveTraining() {
  return apiFetch<{ job: TrainingJob | null }>("/api/train/active/");
}
