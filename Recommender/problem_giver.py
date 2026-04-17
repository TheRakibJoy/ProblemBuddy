"""Recommend unsolved problems from a tier using cosine similarity on tags."""

import logging
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from django.core.cache import cache
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Dataset.codeforces import CodeforcesError, user_status
from Dataset.models import Problem

logger = logging.getLogger(__name__)

VECTORIZER_TTL = 3600


@dataclass
class TierIndex:
    problems: list[Problem]
    vectorizer: CountVectorizer
    vectors: np.ndarray


@dataclass
class Recommendation:
    problem: Problem
    matched_tags: list[str]


def _build_tier_index(tier: str) -> TierIndex | None:
    problems = list(Problem.objects.filter(tier=tier).order_by("id"))
    if not problems:
        return None
    corpus = [p.Tags or "" for p in problems]
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(corpus).toarray()
    return TierIndex(problems=problems, vectorizer=vectorizer, vectors=vectors)


def _tier_index(tier: str) -> TierIndex | None:
    cache_key = f"tier-index:{tier}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    index = _build_tier_index(tier)
    if index is not None:
        cache.set(cache_key, index, VECTORIZER_TTL)
    return index


def invalidate_tier_index(tier: str) -> None:
    cache.delete(f"tier-index:{tier}")


def _solved_problem_keys(handle: str) -> set[tuple[int, str]]:
    try:
        submissions = user_status(handle)
    except CodeforcesError:
        return set()
    solved: set[tuple[int, str]] = set()
    for sub in submissions:
        if sub.get("verdict") != "OK":
            continue
        problem = sub["problem"]
        if "contestId" in problem:
            solved.add((problem["contestId"], problem["index"]))
    return solved


def _problem_tag_set(problem: Problem) -> set[str]:
    return {t.strip() for t in (problem.Tags or "").split(",") if t.strip()}


def recommend(
    *,
    cf_handle: str,
    user_id: int | None,
    weak_tags: str,
    tier: str,
    count: int = 3,
    include_tags: Iterable[str] | None = None,
    exclude_tags: Iterable[str] | None = None,
    min_rating: int | None = None,
    max_rating: int | None = None,
    weak_only: bool = False,
) -> list[Recommendation]:
    """Return up to ``count`` recommendations for the user, respecting filters."""
    index = _tier_index(tier)
    if index is None or not weak_tags:
        return []

    weak_vector = index.vectorizer.transform([weak_tags]).toarray()
    similarity = cosine_similarity(weak_vector, index.vectors)[0]
    ranked = np.argsort(-similarity)

    solved = _solved_problem_keys(cf_handle)
    hidden_problem_ids: set[int] = set()
    if user_id is not None:
        from .models import ProblemInteraction

        hidden_problem_ids = set(
            ProblemInteraction.objects.filter(
                user_id=user_id, status__in=("solved", "not_interested", "hidden")
            ).values_list("problem_id", flat=True)
        )

    include = {t.lower() for t in (include_tags or [])}
    exclude = {t.lower() for t in (exclude_tags or [])}
    weak_tag_set = {t.strip().lower() for t in weak_tags.split(",") if t.strip()}

    results: list[Recommendation] = []
    for i in ranked:
        problem = index.problems[int(i)]
        if (problem.PID, problem.Index) in solved:
            continue
        if problem.id in hidden_problem_ids:
            continue
        if min_rating is not None and (problem.Rating or 0) < min_rating:
            continue
        if max_rating is not None and (problem.Rating or 0) > max_rating:
            continue

        tags = _problem_tag_set(problem)
        tags_lower = {t.lower() for t in tags}
        if include and not include.issubset(tags_lower):
            continue
        if exclude and exclude & tags_lower:
            continue
        matched = sorted(tags_lower & weak_tag_set)
        if weak_only and not matched:
            continue

        results.append(Recommendation(problem=problem, matched_tags=matched))
        if len(results) >= count:
            break
    return results


def give_me_problem(handle: str, weak_tags: str, tier: str) -> list[int]:
    """Legacy signature retained for the classic view path and tests."""
    recs = recommend(
        cf_handle=handle,
        user_id=None,
        weak_tags=weak_tags,
        tier=tier,
        count=10,
    )
    tier_problems = list(Problem.objects.filter(tier=tier).order_by("id"))
    id_to_index = {p.id: idx for idx, p in enumerate(tier_problems)}
    return [id_to_index[r.problem.id] for r in recs if r.problem.id in id_to_index]
