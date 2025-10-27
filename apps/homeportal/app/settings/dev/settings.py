"""Contains dev settings and config."""

from app.settings.core.settings import *  # noqa: F401 F403 F405

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}
