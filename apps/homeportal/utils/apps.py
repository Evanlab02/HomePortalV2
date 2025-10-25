"""Utilities app for some generic config and functions."""

from django.apps import AppConfig


class UtilsConfig(AppConfig):
    """Utils app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "utils"
