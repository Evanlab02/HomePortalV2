"""Contains the URL paths for the API app."""

from typing import Literal

from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI, Schema

api = NinjaAPI(
    title="Home Portal V2 API",
    version="0.7.6",  # x-release-please-version
)


class HealthCheck(Schema):
    """Health check schema for the API."""

    status: Literal["ok"]


@api.get("/health", response={200: HealthCheck})
def health(request: HttpRequest) -> HealthCheck:
    """Health Check."""
    return HealthCheck(status="ok")


urlpatterns = [
    path("", api.urls),
]
