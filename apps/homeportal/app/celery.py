"""Contains the celery config."""

import os

from celery import Celery  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.core.settings")

VALKEY_HOST = os.environ.get("DJANGO_CACHE_HOST", "valkey")
VALKEY_PORT = os.environ.get("DJANGO_CACHE_PORT", "6379")
VALKEY_DB = "0"
VALKEY_URL = f"redis://{VALKEY_HOST}:{VALKEY_PORT}/{VALKEY_DB}"

app = Celery("Django Worker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = VALKEY_URL
app.autodiscover_tasks()
