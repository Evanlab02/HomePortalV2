"""Contains auth permission checks."""

from django.http import HttpRequest


def can_view_users(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view users.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'auth.view_user' permission, False otherwise.
    """
    return request.user.has_perm("auth.view_user")


def can_view_groups(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view groups.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'auth.view_group' permission, False otherwise.
    """
    return request.user.has_perm("auth.view_group")


def can_view_celery_results(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view Celery results.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'django_celery_results.view_taskresult' permission, False otherwise.
    """
    return request.user.has_perm("django_celery_results.view_taskresult")


def can_view_celery_tasks(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view Celery periodic tasks.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'django_celery_beat.view_periodictask' permission, False otherwise.
    """
    return request.user.has_perm("django_celery_beat.view_periodictask")


def can_view_cloudflare_zones(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view Cloudflare zones.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'cloudflare.view_cloudflarezone' permission, False otherwise.
    """
    return request.user.has_perm("cloudflare.view_cloudflarezone")


def can_view_cloudflare_dns_records(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view Cloudflare DNS records.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'cloudflare.view_cloudflarednsrecord' permission, False otherwise.
    """
    return request.user.has_perm("cloudflare.view_cloudflarednsrecord")


def can_view_qbit_servers(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view QBittorrent servers.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'qbit.view_qbitserver' permission, False otherwise.
    """
    return request.user.has_perm("qbit.view_qbitserver")


def can_view_constance_config(request: HttpRequest) -> bool:
    """
    Check if the user has permission to view application configuration.

    Args:
        request: The HTTP request object containing the authenticated user.

    Returns:
        bool: True if the user has the 'constance.view_config' permission, False otherwise.
    """
    return request.user.has_perm("constance.view_config")
