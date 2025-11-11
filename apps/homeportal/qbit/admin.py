"""Admin config for the QBittorrent sync app.

This module provides Django admin configuration for managing QBittorrent servers,
including synchronization capabilities for pulling and pushing configurations.
"""

from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from unfold.decorators import display

from qbit.models import QBitServer
from utils.admin import BaseAdminMixin


@admin.register(QBitServer)
class QBitServerAdmin(BaseAdminMixin):
    """Admin configuration for QBitServer model with sync capabilities.

    Provides an admin interface for managing QBittorrent servers with custom
    actions for synchronizing configuration between the database and QBittorrent servers.
    """

    list_display = ("host", "username", "listen_port", "display_sync_actions")
    list_filter = ("host",)
    search_fields = ("host", "username")
    readonly_fields = ("display_sync_actions_detail",)

    fieldsets = (
        (
            "Server Details",
            {
                "fields": ("host", "username", "password", "listen_port"),
            },
        ),
        (
            "Sync Operations",
            {
                "fields": ("display_sync_actions_detail",),
                "description": "Use these buttons to synchronize configuration between the database and the QBittorrent server.",  # noqa: E501
            },
        ),
    )

    def get_urls(self):
        """Add custom URLs for single-instance sync operations.

        Extends the default admin URLs with custom endpoints for pulling and
        pushing configuration to individual QBittorrent servers.

        Returns:
            urls (list): List of URL patterns including custom sync URLs.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/pull/",
                self.admin_site.admin_view(self.pull_single_view),
                name="qbit_qbitserver_pull",
            ),
            path(
                "<path:object_id>/push/",
                self.admin_site.admin_view(self.push_single_view),
                name="qbit_qbitserver_push",
            ),
        ]
        return custom_urls + urls

    @display(description="Actions", label=True)
    def display_sync_actions(self, obj):
        """Display sync action buttons in list view.

        Renders pull and push action buttons for a QBittorrent server in the admin list view.

        Args:
            obj (QBitServer): The QBitServer instance to display actions for.

        Returns:
            result (str): HTML string containing formatted action buttons.
        """
        pull_url = reverse("admin:qbit_qbitserver_pull", args=[obj.pk])
        push_url = reverse("admin:qbit_qbitserver_push", args=[obj.pk])
        return format_html(
            '<a class="inline-flex items-center justify-center gap-1.5 rounded-md text-sm '
            "font-medium transition-all duration-200 "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-offset-2 focus-visible:ring-blue-500 "
            "bg-blue-600 text-white "
            "hover:bg-blue-700 hover:shadow-md hover:scale-105 "
            'active:scale-95 h-8 px-3 py-2 mr-2 no-underline cursor-pointer" '
            'href="{}" style="display: inline-flex !important;">'
            '<span style="line-height: 1;">⬇</span> '
            '<span style="line-height: 1;">Pull</span>'
            "</a>"
            '<a class="inline-flex items-center justify-center gap-1.5 rounded-md text-sm '
            "font-medium transition-all duration-200 "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-offset-2 focus-visible:ring-green-500 "
            "bg-green-600 text-white "
            "hover:bg-green-700 hover:shadow-md hover:scale-105 "
            'active:scale-95 h-8 px-3 py-2 no-underline cursor-pointer" '
            'href="{}" style="display: inline-flex !important;">'
            '<span style="line-height: 1;">⬆</span> '
            '<span style="line-height: 1;">Push</span>'
            "</a>",
            pull_url,
            push_url,
        )

    @display(description="", label=False)
    def display_sync_actions_detail(self, obj):
        """Display sync action buttons in detail view.

        Renders pull and push action buttons for a QBittorrent server in the admin detail view.
        Shows a message if the object hasn't been saved yet.

        Args:
            obj (QBitServer): The QBitServer instance to display actions for.

        Returns:
            result (str): HTML string containing formatted action buttons or a save prompt message.
        """
        if not obj.pk:
            return "Save the server first to enable sync actions."

        pull_url = reverse("admin:qbit_qbitserver_pull", args=[obj.pk])
        push_url = reverse("admin:qbit_qbitserver_push", args=[obj.pk])
        return format_html(
            '<div class="flex gap-4" style="display: flex; gap: 1rem;">'
            '<a class="inline-flex items-center justify-center gap-2 rounded-md text-sm '
            "font-medium transition-all duration-200 "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-offset-2 focus-visible:ring-blue-500 "
            "bg-blue-600 text-white "
            "hover:bg-blue-700 hover:shadow-lg hover:scale-105 "
            'active:scale-95 h-10 px-4 py-2 no-underline cursor-pointer" '
            'href="{}" style="display: inline-flex !important;">'
            '<span style="line-height: 1; font-size: 1.2em;">⬇</span> '
            '<span style="line-height: 1;">Pull Config from Server</span>'
            "</a>"
            '<a class="inline-flex items-center justify-center gap-2 rounded-md text-sm '
            "font-medium transition-all duration-200 "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-offset-2 focus-visible:ring-green-500 "
            "bg-green-600 text-white "
            "hover:bg-green-700 hover:shadow-lg hover:scale-105 "
            'active:scale-95 h-10 px-4 py-2 no-underline cursor-pointer" '
            'href="{}" style="display: inline-flex !important;">'
            '<span style="line-height: 1; font-size: 1.2em;">⬆</span> '
            '<span style="line-height: 1;">Push Config to Server</span>'
            "</a>"
            "</div>",
            pull_url,
            push_url,
        )

    def pull_single_view(self, request: HttpRequest, object_id: str):
        """Handle pull action for a single server.

        Pulls configuration from a QBittorrent server and updates the database record.
        Displays success or error messages to the user.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The primary key of the QBitServer instance.

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
            self.message_user(
                request,
                f"Error pulling config from {server.host}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:qbit_qbitserver_change", args=[object_id]))

    def push_single_view(self, request: HttpRequest, object_id: str):
        """Handle push action for a single server.

        Pushes configuration from the database to a QBittorrent server.
        Displays success or error messages to the user.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The primary key of the QBitServer instance.

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
            self.message_user(
                request,
                f"Error pushing config to {server.host}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:qbit_qbitserver_change", args=[object_id]))

    @admin.action(description="Pull config from selected servers")
    def bulk_pull_configs(self, request: HttpRequest, queryset):
        """Bulk action to pull configs from multiple servers.

        Iterates through selected servers and pulls configuration from each.
        Displays individual warnings for failures and summary messages for successes.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): QuerySet of selected QBitServer instances.

        Returns:
            result (None): No return value.
        """
        success_count = 0
        error_count = 0

        for server in queryset:
            try:
                session = server.login()
                server.pull(session=session)
                success_count += 1
            except Exception:
                error_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"Successfully pulled configs from {success_count} server(s).",
                level=messages.SUCCESS,
            )

        if error_count > 0:
            self.message_user(
                request,
                f"Failed to pull configs from {error_count} server(s).",
                level=messages.ERROR,
            )

    @admin.action(description="Push config to selected servers")
    def bulk_push_configs(self, request: HttpRequest, queryset):
        """Bulk action to push configs to multiple servers.

        Iterates through selected servers and pushes configuration to each.
        Displays individual warnings for failures and summary messages for successes.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): QuerySet of selected QBitServer instances.

        Returns:
            result (None): No return value.
        """
        success_count = 0
        error_count = 0

        for server in queryset:
            try:
                session = server.login()
                server.push(session=session)
                success_count += 1
            except Exception:
                error_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"Successfully pushed configs to {success_count} server(s).",
                level=messages.SUCCESS,
            )

        if error_count > 0:
            self.message_user(
                request,
                f"Failed to push configs to {error_count} server(s).",
                level=messages.ERROR,
            )

    actions = ["bulk_pull_configs", "bulk_push_configs"]
