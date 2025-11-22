"""Utility models and configuration."""

from django.contrib.auth.models import Group, User
from django.db.models import DateTimeField, Model
from simple_history import register
from simple_history.models import HistoricalRecords

register(User, app=__package__)
register(Group, app=__package__)


class BaseModel(Model):
    """Base model for all app models."""

    class Meta:
        """Meta config for the BaseModel."""

        abstract = True

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)
