def theme_context(request):
    profile = getattr(getattr(request, "user", None), "profile", None)
    return {
        "theme_preference": getattr(profile, "theme_preference", "system") if profile else "system",
    }
