"""Identify a user's weak tags by comparing their recent solves to the tier reference."""

import logging

from Dataset.codeforces import CodeforcesError, user_rating, user_status
from Dataset.constants import COUNTER_TOTAL_TAG
from Dataset.models import Counter

from .Target import get_lo_hi

logger = logging.getLogger(__name__)


def _normalize(tag: str) -> str:
    return tag.replace(" ", "").replace("-", "")


def get_weak_tags(handle: str) -> tuple[str, list[int]]:
    """Return ("tag1, tag2, ...", [pct1, pct2, ...]) for a user's weak tags.

    Returns ("", []) when data is unavailable.
    """
    current, target, tier = get_lo_hi(handle)
    if current == -1:
        return "", []

    try:
        ratings = user_rating(handle)
    except CodeforcesError:
        return "", []

    start = None
    for con in ratings:
        if con["newRating"] >= con["oldRating"] and con["newRating"] >= current:
            ts = con["ratingUpdateTimeSeconds"]
            start = ts if start is None else min(start, ts)
    if start is None:
        return "", []

    try:
        submissions = user_status(handle)
    except CodeforcesError:
        return "", []

    user_tag_counts: dict[str, int] = {}
    for sub in submissions:
        if sub["creationTimeSeconds"] < start or sub["verdict"] != "OK":
            continue
        problem = sub["problem"]
        rating = problem.get("rating")
        if rating is None or rating <= current:
            continue
        tags = [_normalize(t) for t in problem["tags"]] + [str(rating)]
        for tag in tags:
            user_tag_counts[tag] = user_tag_counts.get(tag, 0) + 1

    totals = Counter.objects.filter(tag_name=COUNTER_TOTAL_TAG, tier=tier).first()
    if totals is None or totals.count == 0:
        return "", []

    weak_tags: list[str] = []
    percentage: list[int] = []
    for row in Counter.objects.filter(tier=tier).exclude(tag_name=COUNTER_TOTAL_TAG):
        expected = row.count // totals.count
        if expected <= 0:
            continue
        actual = user_tag_counts.get(row.tag_name, 0)
        if actual < expected:
            percentage.append(round((expected - actual) * 100 / expected))
            weak_tags.append(row.tag_name)

    return ", ".join(weak_tags), percentage
