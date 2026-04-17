"""JSON endpoints that power the React islands."""

import json
import logging
from functools import wraps

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from Dataset.codeforces import CodeforcesError, handle_exists, user_info
from Dataset.constants import RATING_TIERS
from Dataset.models import Problem

from .Target import get_lo_hi
from .models import Profile, ProblemInteraction
from .problem_giver import recommend
from .weak_tags import get_weak_tags

logger = logging.getLogger(__name__)


def login_required_json(view):
    @wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "authentication required"}, status=401)
        return view(request, *args, **kwargs)

    return wrapper


def _cf_handle(request) -> str:
    profile = getattr(request.user, "profile", None)
    if profile and profile.cf_handle:
        return profile.cf_handle
    return request.user.get_username()


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [p.strip() for p in value.split(",") if p.strip()]


def _int_or_none(value: str | None) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _problem_payload(problem: Problem, matched: list[str]) -> dict:
    tags = [t.strip() for t in (problem.Tags or "").split(",") if t.strip()]
    return {
        "id": problem.id,
        "pid": problem.PID,
        "index": problem.Index,
        "rating": problem.Rating,
        "tags": tags,
        "matched_tags": matched,
        "reason": (
            f"matches your weak tags: {', '.join(matched)}" if matched else None
        ),
        "url": f"https://codeforces.com/contest/{problem.PID}/problem/{problem.Index}",
    }


@require_GET
@login_required_json
def recommend_view(request: HttpRequest) -> JsonResponse:
    handle = _cf_handle(request)
    current, target, tier = get_lo_hi(handle)
    if current == -1:
        return JsonResponse(
            {"detail": "codeforces unavailable", "problems": []}, status=503
        )

    profile: Profile = request.user.profile
    count = _int_or_none(request.GET.get("count")) or profile.recommendations_per_load
    count = max(1, min(12, count))

    weak_tags, _pct = get_weak_tags(handle)
    recs = recommend(
        cf_handle=handle,
        user_id=request.user.id,
        weak_tags=weak_tags,
        tier=tier,
        count=count,
        include_tags=_parse_csv(request.GET.get("tags")),
        exclude_tags=_parse_csv(request.GET.get("exclude_tags")),
        min_rating=_int_or_none(request.GET.get("min")),
        max_rating=_int_or_none(request.GET.get("max")),
        weak_only=request.GET.get("weak_only") == "1",
    )
    return JsonResponse(
        {
            "problems": [_problem_payload(r.problem, r.matched_tags) for r in recs],
            "generated_at": now().isoformat(),
            "tier": tier,
            "next_target": target,
        }
    )


@require_POST
@login_required_json
def interactions_view(request: HttpRequest) -> HttpResponse:
    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)
    problem_id = body.get("problem_id")
    status = body.get("status")
    if status not in ("solved", "not_interested", "hidden"):
        return JsonResponse({"detail": "invalid status"}, status=400)
    try:
        problem = Problem.objects.get(pk=problem_id)
    except Problem.DoesNotExist:
        return JsonResponse({"detail": "problem not found"}, status=404)
    ProblemInteraction.objects.update_or_create(
        user=request.user, problem=problem, defaults={"status": status}
    )
    return HttpResponse(status=204)


@require_GET
@login_required_json
def profile_summary_view(request: HttpRequest) -> JsonResponse:
    handle = _cf_handle(request)
    current, target, tier = get_lo_hi(handle)
    info: dict = {}
    if current != -1:
        try:
            info = user_info(handle)
        except CodeforcesError:
            info = {}
    weak_tags_str, percentage = get_weak_tags(handle)
    weak_tags = [t.strip() for t in weak_tags_str.split(",") if t.strip()]
    weak_list = sorted(
        ({"tag": t, "pct": p} for t, p in zip(weak_tags, percentage)),
        key=lambda r: r["pct"],
        reverse=True,
    )
    return JsonResponse(
        {
            "username": request.user.get_username(),
            "email": request.user.email,
            "cf_handle": request.user.profile.cf_handle,
            "max_rating": int(info.get("maxRating", 0)) if info else 0,
            "max_rank": info.get("maxRank", "unrated") if info else "unrated",
            "photo": info.get("titlePhoto") if info else None,
            "tier": tier,
            "current_floor": current,
            "next_target": target,
            "weak_tags": weak_list,
            "tiers": [
                {"floor": floor, "target": tgt, "key": key, "label": label}
                for floor, tgt, key, label in RATING_TIERS
            ],
        }
    )


@require_GET
@login_required_json
def cf_handle_check_view(request: HttpRequest) -> JsonResponse:
    handle = (request.GET.get("handle") or "").strip()
    if not handle:
        return JsonResponse({"detail": "handle required"}, status=400)
    return JsonResponse({"handle": handle, "exists": handle_exists(handle)})


@require_http_methods(["GET", "PATCH"])
@login_required_json
def settings_view(request: HttpRequest) -> JsonResponse:
    profile: Profile = request.user.profile
    if request.method == "GET":
        return JsonResponse(_profile_payload(request.user, profile))

    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)

    if "email" in body:
        request.user.email = body["email"]
        request.user.save(update_fields=["email"])

    if "cf_handle" in body:
        new_handle = (body["cf_handle"] or "").strip() or None
        if new_handle and not handle_exists(new_handle):
            return JsonResponse({"detail": "Codeforces handle not found"}, status=400)
        profile.cf_handle = new_handle

    for field in ("theme_preference", "difficulty_offset", "recommendations_per_load"):
        if field in body:
            setattr(profile, field, body[field])
    profile.save()
    return JsonResponse(_profile_payload(request.user, profile))


def _profile_payload(user, profile: Profile) -> dict:
    return {
        "username": user.get_username(),
        "email": user.email,
        "cf_handle": profile.cf_handle,
        "theme_preference": profile.theme_preference,
        "difficulty_offset": profile.difficulty_offset,
        "recommendations_per_load": profile.recommendations_per_load,
    }


@require_POST
@login_required_json
def account_delete_view(request: HttpRequest) -> HttpResponse:
    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)
    password = body.get("password") or ""
    if not request.user.check_password(password):
        return JsonResponse({"detail": "password incorrect"}, status=403)
    request.user.delete()
    return HttpResponse(status=204)


@require_POST
@login_required_json
def train_enqueue_view(request: HttpRequest) -> JsonResponse:
    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)
    handle = (body.get("handle") or "").strip().lower()
    if not handle:
        return JsonResponse({"detail": "handle required"}, status=400)
    if not handle_exists(handle):
        return JsonResponse({"detail": "Codeforces handle not found"}, status=400)

    from Dataset.tasks import train_handle

    try:
        async_result = train_handle.delay(handle)
        return JsonResponse({"task_id": async_result.id, "handle": handle})
    except Exception:
        logger.exception("failed to enqueue train_handle")
        # Fall back to synchronous execution in dev without a broker.
        from Dataset.add_data import ingest_all_tiers

        ingest_all_tiers(handle)
        return JsonResponse({"task_id": None, "handle": handle, "sync": True})


@require_GET
@login_required_json
def train_status_view(request: HttpRequest, task_id: str) -> JsonResponse:
    try:
        from celery.result import AsyncResult

        result = AsyncResult(task_id)
        return JsonResponse(
            {
                "task_id": task_id,
                "state": result.state,
                "info": result.info if isinstance(result.info, dict) else None,
                "ready": result.ready(),
                "successful": result.successful() if result.ready() else None,
            }
        )
    except Exception:
        logger.exception("failed to look up task status")
        return JsonResponse({"task_id": task_id, "state": "UNKNOWN"}, status=200)
