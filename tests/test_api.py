import json
from unittest.mock import patch

import pytest
import responses
from django.contrib.auth.models import User
from django.test import Client

from Dataset import codeforces as cf
from Dataset.constants import TIER_PUPIL
from Dataset.models import Counter, Problem
from Recommender.models import ProblemInteraction


@pytest.fixture(autouse=True)
def _clear_cache():
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def client_(db):
    return Client()


@pytest.fixture
def auth_client(client_):
    user = User.objects.create_user(username="alice", password="pw12345!")
    user.profile.cf_handle = "alice_cf"
    user.profile.save()
    client_.login(username="alice", password="pw12345!")
    return client_, user


def test_recommend_requires_auth(client_):
    response = client_.get("/api/recommend/")
    assert response.status_code == 401
    assert response.json()["detail"] == "authentication required"


@responses.activate
def test_cf_handle_check(auth_client):
    client_, _ = auth_client
    responses.add(
        responses.GET,
        f"{cf.BASE_URL}/user.info",
        json={"status": "OK", "result": [{"handle": "tourist", "maxRating": 3800}]},
    )
    response = client_.get("/api/cf/handle-check/?handle=tourist")
    assert response.status_code == 200
    data = response.json()
    assert data["exists"] is True
    assert data["handle"] == "tourist"


def test_handle_check_requires_param(auth_client):
    client_, _ = auth_client
    response = client_.get("/api/cf/handle-check/")
    assert response.status_code == 400


@pytest.mark.django_db
def test_interactions_roundtrip(auth_client):
    client_, user = auth_client
    problem = Problem.objects.create(
        tier=TIER_PUPIL, PID=1, Index="A", Rating=1200, Tags="dp"
    )
    response = client_.post(
        "/api/interactions/",
        data=json.dumps({"problem_id": problem.id, "status": "solved"}),
        content_type="application/json",
    )
    assert response.status_code == 204
    assert ProblemInteraction.objects.filter(
        user=user, problem=problem, status="solved"
    ).exists()


def test_interactions_rejects_bad_status(auth_client):
    client_, _ = auth_client
    response = client_.post(
        "/api/interactions/",
        data=json.dumps({"problem_id": 1, "status": "weird"}),
        content_type="application/json",
    )
    assert response.status_code == 400


@responses.activate
def test_settings_patch_updates_profile(auth_client):
    client_, user = auth_client
    responses.add(
        responses.GET,
        f"{cf.BASE_URL}/user.info",
        json={"status": "OK", "result": [{"handle": "petr", "maxRating": 3500}]},
    )
    response = client_.patch(
        "/api/settings/",
        data=json.dumps(
            {
                "cf_handle": "petr",
                "theme_preference": "dark",
                "recommendations_per_load": 8,
                "difficulty_offset": 100,
                "email": "a@b.c",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    user.refresh_from_db()
    user.profile.refresh_from_db()
    assert user.profile.cf_handle == "petr"
    assert user.profile.theme_preference == "dark"
    assert user.profile.recommendations_per_load == 8
    assert user.profile.difficulty_offset == 100
    assert user.email == "a@b.c"


@responses.activate
def test_recommend_returns_problems(auth_client):
    client_, _ = auth_client
    responses.add(
        responses.GET,
        f"{cf.BASE_URL}/user.info",
        json={"status": "OK", "result": [{"handle": "alice_cf", "maxRating": 1100}]},
    )
    responses.add(
        responses.GET,
        f"{cf.BASE_URL}/user.rating",
        json={"status": "OK", "result": [{"newRating": 1150, "oldRating": 1100, "ratingUpdateTimeSeconds": 1}]},
    )
    responses.add(
        responses.GET,
        f"{cf.BASE_URL}/user.status",
        json={
            "status": "OK",
            "result": [
                {
                    "verdict": "OK",
                    "creationTimeSeconds": 10,
                    "problem": {"contestId": 1, "index": "A", "rating": 1200, "tags": ["math"]},
                }
            ],
        },
    )
    Counter.objects.create(tag_name="users", tier=TIER_PUPIL, count=2)
    Counter.objects.create(tag_name="dp", tier=TIER_PUPIL, count=6)
    Counter.objects.create(tag_name="math", tier=TIER_PUPIL, count=4)
    Problem.objects.create(tier=TIER_PUPIL, PID=2, Index="B", Rating=1200, Tags="dp, 1200")
    Problem.objects.create(tier=TIER_PUPIL, PID=3, Index="C", Rating=1300, Tags="math, 1300")

    with patch("Recommender.problem_giver._solved_problem_keys", return_value=set()):
        response = client_.get("/api/recommend/?count=2")
    assert response.status_code == 200
    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) <= 2
    for p in data["problems"]:
        assert set(p.keys()) >= {"id", "pid", "index", "rating", "tags", "url"}
