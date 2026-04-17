import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useCallback, useMemo, useState } from "react";
import { fetchRecommendations, fetchProfileSummary, postInteraction } from "../api/endpoints";
import type { InteractionStatus, Problem } from "../api/types";
import { useToastStore } from "../toast/toastStore";
import { ExplainDrawer } from "./ExplainDrawer";
import { FilterBar, Filters } from "./FilterBar";
import { ProblemCard } from "./ProblemCard";
import { SkeletonCard } from "./SkeletonCard";
import { readFiltersFromUrl } from "./useFiltersFromUrl";

interface BootProps {
  initial_count?: number;
}

export function RecommendPage({ initial_count = 3 }: BootProps) {
  const defaults: Filters = useMemo(
    () => ({
      tags: [],
      exclude_tags: [],
      min: 800,
      max: 3500,
      weak_only: false,
      count: initial_count,
    }),
    [initial_count],
  );
  const [filters, setFilters] = useState<Filters>(() => readFiltersFromUrl(defaults));
  const [explaining, setExplaining] = useState<Problem | null>(null);
  const queryClient = useQueryClient();
  const push = useToastStore((s) => s.push);

  const query = useQuery({
    queryKey: ["recommend", filters],
    queryFn: () =>
      fetchRecommendations({
        count: filters.count,
        tags: filters.tags,
        exclude_tags: filters.exclude_tags,
        min: filters.min,
        max: filters.max,
        weak_only: filters.weak_only,
      }),
    staleTime: 60_000,
  });

  const profileQuery = useQuery({
    queryKey: ["profile-summary"],
    queryFn: fetchProfileSummary,
    staleTime: 5 * 60_000,
  });

  const interact = useMutation({
    mutationFn: ({ problem_id, status }: { problem_id: number; status: InteractionStatus }) =>
      postInteraction(problem_id, status),
    onError: () => push("Could not save your response.", "danger"),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["recommend"] }),
  });

  const handleInteraction = useCallback(
    (problem: Problem, status: InteractionStatus) => {
      interact.mutate({ problem_id: problem.id, status });
      push(
        status === "solved" ? "Nice — marked as solved." : "Noted, we'll skip that one.",
        status === "solved" ? "success" : "info",
      );
    },
    [interact, push],
  );

  const refresh = () =>
    queryClient.invalidateQueries({ queryKey: ["recommend", filters] });

  const slots = Array.from({ length: filters.count });

  return (
    <>
      <section className="text-center mb-4">
        <h3>Solve these problems and improve</h3>
        <p className="text-muted mb-0">
          Recommendations are tailored to your weak tags at the next rating tier.
        </p>
      </section>

      <FilterBar initial={filters} onChange={setFilters} />

      {query.isError && (
        <div className="alert alert-warning">
          Couldn&apos;t load recommendations right now. Try again in a moment.
        </div>
      )}

      <div className="row g-3">
        {query.isLoading || query.isFetching
          ? slots.map((_, i) => (
              <div key={i} className="col-md-4">
                <SkeletonCard />
              </div>
            ))
          : (query.data?.problems ?? []).map((problem) => (
              <div key={problem.id} className="col-md-4">
                <ProblemCard
                  problem={problem}
                  onMarkSolved={(p) => handleInteraction(p, "solved")}
                  onNotInterested={(p) => handleInteraction(p, "not_interested")}
                  onExplain={setExplaining}
                />
              </div>
            ))}
      </div>

      {!query.isLoading && (query.data?.problems.length ?? 0) === 0 && (
        <div className="alert alert-warning text-center mt-3">
          No matches for the current filters. Loosen the tag list or widen the rating range.
        </div>
      )}

      <div className="text-center mt-4">
        <button className="btn btn-outline-primary" onClick={refresh}>
          Get more problems
        </button>
      </div>

      {explaining && (
        <div
          className="offcanvas-backdrop fade show"
          onClick={() => setExplaining(null)}
          aria-hidden="true"
        />
      )}
      <ExplainDrawer
        problem={explaining}
        weakTags={profileQuery.data?.weak_tags ?? []}
        onClose={() => setExplaining(null)}
      />
    </>
  );
}
