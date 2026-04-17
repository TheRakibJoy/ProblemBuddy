"""Thin wrapper around the Codeforces public API with caching + error handling."""

import logging
from typing import Any

import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

BASE_URL = "https://codeforces.com/api"
DEFAULT_TIMEOUT = 10
CACHE_TTL = 600  # 10 minutes


class CodeforcesError(Exception):
    """Raised when the Codeforces API is unreachable or returns an error."""


def _get(endpoint: str, params: dict[str, Any], cache_key: str) -> Any:
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Codeforces API call failed: %s params=%s err=%s", endpoint, params, exc)
        raise CodeforcesError(str(exc)) from exc
    if payload.get("status") != "OK":
        raise CodeforcesError(payload.get("comment", "unknown Codeforces error"))
    result = payload["result"]
    cache.set(cache_key, result, CACHE_TTL)
    return result


def user_info(handle: str) -> dict[str, Any]:
    result = _get("user.info", {"handles": handle}, f"cf:user.info:{handle}")
    if not result:
        raise CodeforcesError(f"no info for handle {handle}")
    return result[0]


def user_rating(handle: str) -> list[dict[str, Any]]:
    return _get("user.rating", {"handle": handle}, f"cf:user.rating:{handle}")


def user_status(handle: str) -> list[dict[str, Any]]:
    return _get(
        "user.status",
        {"handle": handle, "from": 1},
        f"cf:user.status:{handle}",
    )


def handle_exists(handle: str) -> bool:
    try:
        user_info(handle)
        return True
    except CodeforcesError:
        return False
