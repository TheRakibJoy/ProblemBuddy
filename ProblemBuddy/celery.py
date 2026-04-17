"""Celery application bootstrap. Broker/result URLs come from the environment."""

import os

from celery import Celery
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProblemBuddy.settings.dev")

app = Celery(
    "problembuddy",
    broker=config("CELERY_BROKER_URL", default=config("REDIS_URL", default="memory://")),
    backend=config("CELERY_RESULT_BACKEND", default=config("REDIS_URL", default="cache+memory://")),
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
