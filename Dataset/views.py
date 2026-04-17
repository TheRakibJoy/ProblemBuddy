from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from Recommender.decorators import allowed_user

from .add_data import ingest_all_tiers
from .codeforces import handle_exists
from .models import Handle


@login_required(login_url="login")
@allowed_user(["admin"])
def Train(request):
    if request.method != "POST":
        return render(request, "input_handle.html")

    handle = (request.POST.get("handle") or "").strip().lower()
    if not handle:
        messages.error(request, "Handle is required.")
        return redirect("train")

    if Handle.objects.filter(handle=handle).exists():
        messages.error(request, f"Handle {handle!r} is already trained.")
        return redirect("train")

    if not handle_exists(handle):
        messages.error(request, f"Codeforces handle {handle!r} not found.")
        return redirect("train")

    Handle.objects.create(handle=handle)
    ingest_all_tiers(handle)
    messages.success(request, f"Data trained for handle: {handle}")
    return redirect("train")
