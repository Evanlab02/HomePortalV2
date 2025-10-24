"""Utility models and configuration."""

from django.contrib.auth.models import Group, User
from simple_history import register

register(User, app=__package__)
register(Group, app=__package__)
