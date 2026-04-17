from unittest.mock import patch

import pytest

from Dataset.constants import COUNTER_TOTAL_TAG, TIER_PUPIL
from Dataset.models import Counter
from Recommender.weak_tags import get_weak_tags


@pytest.fixture
def pupil_counters(db):
    Counter.objects.create(tag_name=COUNTER_TOTAL_TAG, tier=TIER_PUPIL, count=2)
    Counter.objects.create(tag_name="dp", tier=TIER_PUPIL, count=10)
    Counter.objects.create(tag_name="math", tier=TIER_PUPIL, count=6)


@patch("Recommender.weak_tags.get_lo_hi", return_value=(0, 1200, TIER_PUPIL))
@patch("Recommender.weak_tags.user_rating")
@patch("Recommender.weak_tags.user_status")
def test_weak_tags_flags_underrepresented(status, rating, _target, pupil_counters):
    rating.return_value = [
        {"newRating": 1250, "oldRating": 1100, "ratingUpdateTimeSeconds": 100},
    ]
    status.return_value = [
        {
            "verdict": "OK",
            "creationTimeSeconds": 200,
            "problem": {"rating": 1200, "tags": ["math"]},
        },
    ]
    tags_str, percentage = get_weak_tags("user")
    tags = [t.strip() for t in tags_str.split(",")]
    # dp: expected 5/user, actual 0 → weak. math: expected 3, actual 1 → weak.
    assert "dp" in tags
    assert "math" in tags
    assert all(0 <= p <= 100 for p in percentage)


@patch("Recommender.weak_tags.get_lo_hi", return_value=(-1, -1, ""))
def test_weak_tags_empty_when_handle_unknown(_target):
    assert get_weak_tags("ghost") == ("", [])
