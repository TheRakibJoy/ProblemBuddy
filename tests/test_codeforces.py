import pytest
import responses

from Dataset import codeforces
from Dataset.codeforces import CodeforcesError, handle_exists, user_info


@pytest.fixture(autouse=True)
def clear_cache():
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


@responses.activate
def test_user_info_ok():
    responses.add(
        responses.GET,
        f"{codeforces.BASE_URL}/user.info",
        json={"status": "OK", "result": [{"handle": "tourist", "maxRating": 3500}]},
        status=200,
    )
    assert user_info("tourist")["maxRating"] == 3500


@responses.activate
def test_user_info_failure_raises():
    responses.add(
        responses.GET,
        f"{codeforces.BASE_URL}/user.info",
        json={"status": "FAILED", "comment": "nope"},
        status=200,
    )
    with pytest.raises(CodeforcesError):
        user_info("ghost")


@responses.activate
def test_handle_exists_false_on_error():
    responses.add(
        responses.GET,
        f"{codeforces.BASE_URL}/user.info",
        json={"status": "FAILED", "comment": "not found"},
        status=200,
    )
    assert handle_exists("ghost") is False
