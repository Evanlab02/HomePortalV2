"""Contains the configuration for cloudflare app."""

from django.apps import AppConfig


class CloudflareConfig(AppConfig):
    """Cloudflare Sync App Config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cloudflare"
