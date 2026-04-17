"""Recommend unsolved problems from a tier using cosine similarity on tags."""

import logging
from dataclasses import dataclass

import numpy as np
from django.core.cache import cache
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Dataset.codeforces import CodeforcesError, user_status
from Dataset.models import Problem

logger = logging.getLogger(__name__)

VECTORIZER_TTL = 3600  # 1 hour; invalidated whenever Problem rows change.


@dataclass
class TierIndex:
    problems: list[Problem]
    vectorizer: CountVectorizer
    vectors: np.ndarray


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
    """Return the set of (contestId, index) the handle has solved (best-effort)."""
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


def give_me_problem(handle: str, weak_tags: str, tier: str) -> list[int]:
    """Return indexes into ``Problem.objects.filter(tier=tier).order_by('id')``."""
    index = _tier_index(tier)
    if index is None or not weak_tags:
        return []

    weak_vector = index.vectorizer.transform([weak_tags]).toarray()
    similarity = cosine_similarity(weak_vector, index.vectors)[0]
    ranked = np.argsort(-similarity)

    solved = _solved_problem_keys(handle)
    recommendations: list[int] = []
    for i in ranked:
        problem = index.problems[i]
        if (problem.PID, problem.Index) in solved:
            continue
        recommendations.append(int(i))
        if len(recommendations) >= 10:
            break
    return recommendations
