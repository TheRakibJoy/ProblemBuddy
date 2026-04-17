"""Ingest a reference handle's solved problems into Problem/Counter tables."""

import logging

from django.db import models

from .codeforces import CodeforcesError, user_rating, user_status
from .constants import COUNTER_TOTAL_TAG, RATING_TIERS, TIER_BY_TARGET
from .models import Counter, Problem

logger = logging.getLogger(__name__)


def _bump_counter(tag: str, tier: str) -> None:
    Counter.objects.get_or_create(tag_name=tag, tier=tier, defaults={"count": 0})
    Counter.objects.filter(tag_name=tag, tier=tier).update(count=models.F("count") + 1)


def _normalize_tag(tag: str) -> str:
    return tag.replace(" ", "").replace("-", "")


def _compute_window(ratings: list[dict], current: int, target: int) -> tuple[int, int] | None:
    """Find (start, end) timestamps while the handle climbed from current → target."""
    start = 0
    end = 0
    climbed = False
    for con in ratings:
        if start == 0 and con["newRating"] >= current and con["oldRating"] != 0:
            start = con["ratingUpdateTimeSeconds"]
        if start:
            end = con["ratingUpdateTimeSeconds"]
        if con["newRating"] >= target:
            climbed = True
            break
    return (start, end) if climbed else None


def ingest_handle(handle: str, current: int, target: int) -> int:
    """Ingest submissions for a handle at a given tier. Returns problems added."""
    tier = TIER_BY_TARGET[target]
    try:
        ratings = user_rating(handle)
    except CodeforcesError:
        return 0

    window = _compute_window(ratings, current, target)
    if window is None:
        return 0
    start, end = window

    _bump_counter(COUNTER_TOTAL_TAG, tier)

    try:
        submissions = user_status(handle)
    except CodeforcesError:
        return 0

    added = 0
    for sub in submissions:
        if not (start <= sub["creationTimeSeconds"] <= end):
            continue
        if sub["verdict"] != "OK":
            continue
        problem = sub["problem"]
        rating = problem.get("rating")
        if rating is None or rating <= current:
            continue
        con_id = sub["contestId"]
        index = problem["index"]
        tags = [_normalize_tag(t) for t in problem["tags"]] + [str(rating)]
        for tag in tags:
            _bump_counter(tag, tier)
        _, created = Problem.objects.get_or_create(
            tier=tier,
            PID=con_id,
            Index=index,
            defaults={"Rating": rating, "Tags": ", ".join(tags)},
        )
        if created:
            added += 1
    logger.info("Ingested %d new problems for %s @ tier %s", added, handle, tier)
    return added


def ingest_all_tiers(handle: str) -> None:
    prev_target = 0
    for _floor, target, _tier, _label in RATING_TIERS:
        ingest_handle(handle, prev_target, target)
        prev_target = target
