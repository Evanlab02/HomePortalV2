"""Contains the configuration for qbit app."""

from django.apps import AppConfig


class QbitConfig(AppConfig):
    """QBittorrent Sync App Config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "qbit"
