"""Development settings. Never use in production."""

import os

os.environ.setdefault("DJANGO_SECRET_KEY", "dev-insecure-do-not-use-in-prod")
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

from .base import *  # noqa: E402, F401, F403

INTERNAL_IPS = ["127.0.0.1"]
