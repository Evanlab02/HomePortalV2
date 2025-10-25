"""Contains admin settings and config."""

from app.settings.core.settings import *  # noqa: F401 F403

DEBUG = False
ROOT_URLCONF = "app.settings.admin.urls"
