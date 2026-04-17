from django.apps import AppConfig


class RecommenderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Recommender"

    def ready(self):
        from . import signals  # noqa: F401
