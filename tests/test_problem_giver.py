from unittest.mock import patch

import pytest

from Dataset.constants import TIER_PUPIL
from Dataset.models import Problem
from Recommender.problem_giver import give_me_problem, invalidate_tier_index


@pytest.fixture
def pupil_problems(db):
    Problem.objects.create(tier=TIER_PUPIL, PID=1, Index="A", Rating=1200, Tags="dp, math, 1200")
    Problem.objects.create(tier=TIER_PUPIL, PID=2, Index="B", Rating=1300, Tags="greedy, math, 1300")
    Problem.objects.create(tier=TIER_PUPIL, PID=3, Index="C", Rating=1400, Tags="graphs, dfs, 1400")
    invalidate_tier_index(TIER_PUPIL)
    yield


@patch("Recommender.problem_giver._solved_problem_keys", return_value=set())
def test_give_me_problem_ranks_by_tag_match(_mock, pupil_problems):
    indices = give_me_problem("user", "dp, math", TIER_PUPIL)
    assert indices  # non-empty
    # first hit should be the dp+math problem
    top = Problem.objects.filter(tier=TIER_PUPIL).order_by("id")[indices[0]]
    assert top.PID == 1


@patch("Recommender.problem_giver._solved_problem_keys", return_value={(1, "A")})
def test_give_me_problem_skips_solved(_mock, pupil_problems):
    indices = give_me_problem("user", "dp, math", TIER_PUPIL)
    problems = list(Problem.objects.filter(tier=TIER_PUPIL).order_by("id"))
    for i in indices:
        assert (problems[i].PID, problems[i].Index) != (1, "A")


def test_give_me_problem_empty_tier(db):
    assert give_me_problem("user", "dp", TIER_PUPIL) == []
