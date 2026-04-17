from django.contrib import admin

from .models import Counter, Handle, Problem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("tier", "PID", "Index", "Rating")
    list_filter = ("tier",)
    search_fields = ("PID", "Tags")


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ("tag_name", "tier", "count")
    list_filter = ("tier",)
    search_fields = ("tag_name",)


admin.site.register(Handle)
