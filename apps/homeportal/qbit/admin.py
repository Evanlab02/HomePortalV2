"""Admin config for the QBittorrent sync app.

This module provides Django admin configuration for managing QBittorrent servers,
including synchronization capabilities for pulling and pushing configurations.
"""

from logging import getLogger

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from unfold.decorators import action

from qbit.models import QBitServer
from qbit.tasks import (
    pull_all_qbit_servers,
    pull_qbit_server,
    push_all_qbit_servers,
    push_qbit_server,
)
from utils.admin import BaseAdminMixin

log = getLogger(__name__)


@admin.register(QBitServer)
class QBitServerAdmin(BaseAdminMixin):
    """Admin configuration for QBitServer model with sync capabilities.

    Provides an admin interface for managing QBittorrent servers with custom
    actions for synchronizing configuration between the database and QBittorrent servers.
    """

    list_display = ("host", "username", "listen_port")
    list_filter = ("host",)
    search_fields = ("host", "username")

    fieldsets = (
        (
            "Server Details",
            {
                "fields": ("host", "username", "password", "listen_port"),
            },
        ),
    )

    # Action configurations
    actions_list = [
        {
            "title": "Sync Actions",
            "items": ["pull_all_servers", "push_all_servers"],
        }
    ]
    actions = ["bulk_pull_servers", "bulk_push_servers"]
    actions_row = ["pull_server", "push_server"]
    actions_detail = [
        {
            "title": "Sync Actions",
            "items": ["pull_server", "push_server"],
        }
    ]

    # List actions (header actions)
    @action(
        description="Pull All Servers",
        url_path="pull-all-servers",
        permissions=["pull_all_servers"],
    )
    def pull_all_servers(self, request: HttpRequest):
        """Queue async task to pull config from all QBittorrent servers.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            result (HttpResponseRedirect): Redirect to the changelist page.
        """
        try:
            pull_all_qbit_servers.delay()
            self.message_user(request, "Queued Server Pull", level=messages.SUCCESS)
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(request, f"Error: {str(e)}", level=messages.ERROR)
        return HttpResponseRedirect(reverse("admin:qbit_qbitserver_changelist"))

    @action(
        description="Push All Servers",
        url_path="push-all-servers",
        permissions=["push_all_servers"],
    )
    def push_all_servers(self, request: HttpRequest):
        """Queue async task to push config to all QBittorrent servers.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            result (HttpResponseRedirect): Redirect to the changelist page.
        """
        try:
            push_all_qbit_servers.delay()
            self.message_user(request, "Queued Server Push", level=messages.SUCCESS)
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(request, f"Error: {str(e)}", level=messages.ERROR)
        return HttpResponseRedirect(reverse("admin:qbit_qbitserver_changelist"))

    # Bulk actions (queryset actions)
    @admin.action(description="Pull config from selected servers")
    def bulk_pull_servers(self, request: HttpRequest, queryset: QuerySet[QBitServer]):
        """Queue async tasks to pull configs from selected servers.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): QuerySet of selected QBitServer instances.
        """
        try:
            for server in queryset:
                pull_qbit_server.delay(db_id=server.id)
            self.message_user(request, "Queued Server Pulls", level=messages.SUCCESS)
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(request, f"Error: {str(e)}", level=messages.ERROR)

    @admin.action(description="Push config to selected servers")
    def bulk_push_servers(self, request: HttpRequest, queryset: QuerySet[QBitServer]):
        """Queue async tasks to push configs to selected servers.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): QuerySet of selected QBitServer instances.
        """
        try:
            for server in queryset:
                push_qbit_server.delay(db_id=server.id)
            self.message_user(request, "Queued Server Pushes", level=messages.SUCCESS)
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(request, f"Error: {str(e)}", level=messages.ERROR)

    # Row and detail actions
    @action(
        description="Pull Server Config",
        url_path="pull-server",
        permissions=["pull_server"],
    )
    def pull_server(self, request: HttpRequest, object_id: int):
        """Pull configuration from a single QBittorrent server (synchronous).

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The primary key of the QBitServer instance.

        Returns:
            result (HttpResponseRedirect): Redirect to the server's change page.
        """
        server = self.get_object(request, object_id)
        if server is None:
            self.message_user(request, "Server not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:qbit_qbitserver_changelist"))

        try:
            session = server.login()
            server.pull(session=session)
            self.message_user(
                request,
                f"Successfully pulled config from {server.host}. Listen port: {server.listen_port}",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error pulling config from {server.host}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:qbit_qbitserver_change", args=[object_id]))

    @action(
        description="Push Server Config",
        url_path="push-server",
        permissions=["push_server"],
    )
    def push_server(self, request: HttpRequest, object_id: int):
        """Push configuration to a single QBittorrent server (synchronous).

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The primary key of the QBitServer instance.

        Returns:
            result (HttpResponseRedirect): Redirect to the server's change page.
        """
        server = self.get_object(request, object_id)
        if server is None:
            self.message_user(request, "Server not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:qbit_qbitserver_changelist"))

        try:
            session = server.login()
            server.push(session=session)
            self.message_user(
                request,
                f"Successfully pushed config to {server.host}. Listen port: {server.listen_port}",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error pushing config to {server.host}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:qbit_qbitserver_change", args=[object_id]))

    # Permission methods
    def has_pull_server_permission(
        self, _request: HttpRequest, _obj: QBitServer | None = None
    ) -> bool:
        """Check if user has permission to pull server config.

        Args:
            _request (HttpRequest): The HTTP request object.
            _obj (QBitServer | None): Optional QBitServer instance.

        Returns:
            result (bool): True if user has permission.
        """
        return True

    def has_push_server_permission(
        self, _request: HttpRequest, _obj: QBitServer | None = None
    ) -> bool:
        """Check if user has permission to push server config.

        Args:
            _request (HttpRequest): The HTTP request object.
            _obj (QBitServer | None): Optional QBitServer instance.

        Returns:
            result (bool): True if user has permission.
        """
        return True

    def has_pull_all_servers_permission(self, _request: HttpRequest) -> bool:
        """Check if user has permission to pull all servers.

        Args:
            _request (HttpRequest): The HTTP request object.

        Returns:
            result (bool): True if user has permission.
        """
        return True

    def has_push_all_servers_permission(self, _request: HttpRequest) -> bool:
        """Check if user has permission to push all servers.

        Args:
            _request (HttpRequest): The HTTP request object.

        Returns:
            result (bool): True if user has permission.
        """
        return True
