"""Canonical rating-tier definitions shared across the project."""

TIER_PUPIL = "pupil"
TIER_SPECIALIST = "specialist"
TIER_EXPERT = "expert"
TIER_CANDIDATE_MASTER = "candidate_master"
TIER_MASTER = "master"
TIER_INTL_MASTER = "international_master"
TIER_GRANDMASTER = "grandmaster"
TIER_INTL_GRANDMASTER = "international_grandmaster"
TIER_LEGENDARY = "legendary_grandmaster"

# Ordered low → high. Each entry: (floor_rating, target_rating, tier_key, display_name).
# Floors match the Codeforces rating tier boundaries; target_rating is the next boundary,
# so users are always trained against the next tier they can realistically reach.
RATING_TIERS = [
    (0, 1200, TIER_PUPIL, "Pupil"),
    (1200, 1400, TIER_SPECIALIST, "Specialist"),
    (1400, 1600, TIER_EXPERT, "Expert"),
    (1600, 1900, TIER_CANDIDATE_MASTER, "Candidate Master"),
    (1900, 2100, TIER_MASTER, "Master"),
    (2100, 2300, TIER_INTL_MASTER, "International Master"),
    (2300, 2400, TIER_GRANDMASTER, "Grandmaster"),
    (2400, 2600, TIER_INTL_GRANDMASTER, "International Grandmaster"),
    (2600, 3000, TIER_LEGENDARY, "Legendary Grandmaster"),
]

TIER_CHOICES = [(key, label) for _, _, key, label in RATING_TIERS]

# {target_rating: tier_key}
TIER_BY_TARGET = {target: key for _, target, key, _ in RATING_TIERS}

# Sentinel row in Counter that stores the total user count per tier.
COUNTER_TOTAL_TAG = "users"


def tier_for_max_rating(max_rating: int) -> tuple[int, int, str]:
    """Return (current_floor, target_rating, tier_key) for the given user max rating.

    The highest tier is capped at Master (target 2100).
    """
    chosen = RATING_TIERS[0]
    for floor, target_rating, key, label in RATING_TIERS:
        if max_rating >= floor:
            chosen = (floor, target_rating, key, label)
    floor, target_rating, key, _ = chosen
    return floor, target_rating, key
