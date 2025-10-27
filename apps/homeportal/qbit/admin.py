"""
Admin config for the QBittorrent sync app.
"""

from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from unfold.decorators import display

from app.exceptions import HomePortalHTTPError
from qbit.models import QBitServer
from utils.admin import BaseAdminMixin


@admin.register(QBitServer)
class QBitServerAdmin(BaseAdminMixin):
    """Admin configuration for QBitServer model with sync capabilities."""

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
                "description": "Use these buttons to synchronize configuration between the database and the QBittorrent server.",
            },
        ),
    )

    def get_urls(self):
        """Add custom URLs for single-instance sync operations."""
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
        """Display sync action buttons in list view."""
        pull_url = reverse("admin:qbit_qbitserver_pull", args=[obj.pk])
        push_url = reverse("admin:qbit_qbitserver_push", args=[obj.pk])
        return format_html(
            '<a class="inline-flex items-center justify-center rounded-md text-sm font-medium '
            'ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 '
            'focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none '
            'disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-8 px-3 py-2 mr-2" '
            'href="{}">⬇ Pull</a>'
            '<a class="inline-flex items-center justify-center rounded-md text-sm font-medium '
            'ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 '
            'focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none '
            'disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-8 px-3 py-2" '
            'href="{}">⬆ Push</a>',
            pull_url,
            push_url,
        )

    @display(description="", label=False)
    def display_sync_actions_detail(self, obj):
        """Display sync action buttons in detail view."""
        if not obj.pk:
            return "Save the server first to enable sync actions."

        pull_url = reverse("admin:qbit_qbitserver_pull", args=[obj.pk])
        push_url = reverse("admin:qbit_qbitserver_push", args=[obj.pk])
        return format_html(
            '<div class="flex gap-4">'
            '<a class="inline-flex items-center justify-center rounded-md text-sm font-medium '
            'ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 '
            'focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none '
            'disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2" '
            'href="{}">⬇ Pull Config from Server</a>'
            '<a class="inline-flex items-center justify-center rounded-md text-sm font-medium '
            'ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 '
            'focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none '
            'disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2" '
            'href="{}">⬆ Push Config to Server</a>'
            '</div>',
            pull_url,
            push_url,
        )

    def pull_single_view(self, request: HttpRequest, object_id: str):
        """Handle pull action for a single server."""
        server = self.get_object(request, object_id)
        if server is None:
            self.message_user(
                request, "Server not found.", level=messages.ERROR
            )
            return HttpResponseRedirect(reverse("admin:qbit_qbitserver_changelist"))

        try:
            session = server.login()
            server.pull(session=session)
            self.message_user(
                request,
                f"Successfully pulled config from {server.host}. Listen port: {server.listen_port}",
                level=messages.SUCCESS,
            )
        except HomePortalHTTPError as e:
            self.message_user(
                request,
                f"Failed to pull config from {server.host}: HTTP {e.status}",
                level=messages.ERROR,
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error pulling config from {server.host}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:qbit_qbitserver_change", args=[object_id])
        )

    def push_single_view(self, request: HttpRequest, object_id: str):
        """Handle push action for a single server."""
        server = self.get_object(request, object_id)
        if server is None:
            self.message_user(
                request, "Server not found.", level=messages.ERROR
            )
            return HttpResponseRedirect(reverse("admin:qbit_qbitserver_changelist"))

        try:
            session = server.login()
            server.push(session=session)
            self.message_user(
                request,
                f"Successfully pushed config to {server.host}. Listen port: {server.listen_port}",
                level=messages.SUCCESS,
            )
        except HomePortalHTTPError as e:
            self.message_user(
                request,
                f"Failed to push config to {server.host}: HTTP {e.status}",
                level=messages.ERROR,
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error pushing config to {server.host}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:qbit_qbitserver_change", args=[object_id])
        )

    @admin.action(description="Pull config from selected servers")
    def bulk_pull_configs(self, request: HttpRequest, queryset):
        """Bulk action to pull configs from multiple servers."""
        success_count = 0
        error_count = 0

        for server in queryset:
            try:
                session = server.login()
                server.pull(session=session)
                success_count += 1
            except HomePortalHTTPError as e:
                error_count += 1
                self.message_user(
                    request,
                    f"Failed to pull from {server.host}: HTTP {e.status}",
                    level=messages.WARNING,
                )
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    f"Error pulling from {server.host}: {str(e)}",
                    level=messages.WARNING,
                )

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
        """Bulk action to push configs to multiple servers."""
        success_count = 0
        error_count = 0

        for server in queryset:
            try:
                session = server.login()
                server.push(session=session)
                success_count += 1
            except HomePortalHTTPError as e:
                error_count += 1
                self.message_user(
                    request,
                    f"Failed to push to {server.host}: HTTP {e.status}",
                    level=messages.WARNING,
                )
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    f"Error pushing to {server.host}: {str(e)}",
                    level=messages.WARNING,
                )

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
