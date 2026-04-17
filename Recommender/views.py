from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .decorators import unauthenticated_user
from .forms import CreateUserForm


def Home(request):
    return render(request, "home.html")


@unauthenticated_user
def LogIn(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not getattr(user.profile, "cf_handle", None):
                return redirect("onboarding")
            return redirect("home")
        messages.info(request, "Username or Password is incorrect.")
    return render(request, "login.html")


@require_POST
@login_required(login_url="login")
def LogOut(request):
    logout(request)
    return redirect("login")


@unauthenticated_user
def Register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            handle = form.cleaned_data.get("username")
            group, _ = Group.objects.get_or_create(name="contestant")
            user.groups.add(group)
            messages.success(request, f"Account was created for user {handle}")
            return redirect("login")
    return render(request, "register.html", {"form": form})


def _needs_onboarding(request) -> bool:
    if not request.user.is_authenticated:
        return False
    profile = getattr(request.user, "profile", None)
    return not (profile and profile.cf_handle)


@login_required(login_url="login")
def Onboarding(request):
    return render(request, "onboarding.html")


@login_required(login_url="login")
def Recommend(request):
    if _needs_onboarding(request):
        return redirect("onboarding")
    return render(request, "recommend.html")


@login_required(login_url="login")
def Profile(request):
    if _needs_onboarding(request):
        return redirect("onboarding")
    return render(request, "profile.html")


@login_required(login_url="login")
def Settings(request):
    return render(request, "settings.html")
