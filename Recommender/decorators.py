from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_user(allowed_roles=None):
    allowed = set(allowed_roles or [])

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and (
                user.is_superuser or user.groups.filter(name__in=allowed).exists()
            ):
                return view_func(request, *args, **kwargs)
            return HttpResponse(
                "You are not authorized. Please contact the admin for access",
                status=403,
            )

        return wrapper_func

    return decorator
