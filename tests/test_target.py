import pytest

from Dataset.constants import (
    TIER_CANDIDATE_MASTER,
    TIER_EXPERT,
    TIER_GRANDMASTER,
    TIER_INTL_GRANDMASTER,
    TIER_INTL_MASTER,
    TIER_LEGENDARY,
    TIER_MASTER,
    TIER_PUPIL,
    TIER_SPECIALIST,
    tier_for_max_rating,
)


@pytest.mark.parametrize(
    "rating,expected",
    [
        (0, (0, 1200, TIER_PUPIL)),
        (1199, (0, 1200, TIER_PUPIL)),
        (1200, (1200, 1400, TIER_SPECIALIST)),
        (1399, (1200, 1400, TIER_SPECIALIST)),
        (1400, (1400, 1600, TIER_EXPERT)),
        (1599, (1400, 1600, TIER_EXPERT)),
        (1600, (1600, 1900, TIER_CANDIDATE_MASTER)),
        (1899, (1600, 1900, TIER_CANDIDATE_MASTER)),
        (1900, (1900, 2100, TIER_MASTER)),
        (2099, (1900, 2100, TIER_MASTER)),
        (2100, (2100, 2300, TIER_INTL_MASTER)),
        (2299, (2100, 2300, TIER_INTL_MASTER)),
        (2300, (2300, 2400, TIER_GRANDMASTER)),
        (2399, (2300, 2400, TIER_GRANDMASTER)),
        (2400, (2400, 2600, TIER_INTL_GRANDMASTER)),
        (2599, (2400, 2600, TIER_INTL_GRANDMASTER)),
        (2600, (2600, 3000, TIER_LEGENDARY)),
        (3500, (2600, 3000, TIER_LEGENDARY)),
    ],
)
def test_tier_for_max_rating(rating, expected):
    assert tier_for_max_rating(rating) == expected
