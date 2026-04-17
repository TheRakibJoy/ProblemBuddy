"""Map a Codeforces handle to its (current_floor, target_rating, tier) triple."""

from Dataset.codeforces import CodeforcesError, user_info
from Dataset.constants import tier_for_max_rating


def get_lo_hi(handle: str) -> tuple[int, int, str]:
    """Return (current_floor, target_rating, tier_key).

    Returns (-1, -1, "") if the handle cannot be resolved.
    """
    try:
        info = user_info(handle)
    except CodeforcesError:
        return -1, -1, ""
    max_rating = int(info.get("maxRating", 0))
    return tier_for_max_rating(max_rating)
