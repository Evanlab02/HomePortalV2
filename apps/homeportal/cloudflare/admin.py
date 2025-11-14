"""Admin config for the Cloudflare app."""

from logging import getLogger

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from unfold.decorators import action

from cloudflare.models import CloudflareDNSRecord, CloudflareZone
from cloudflare.tasks import sync_cloudflare_zones, sync_cloudflare_zone, sync_cloudflare_zone_dns_records
from utils.admin import BaseAdminMixin

log = getLogger(__name__)


@admin.register(CloudflareZone)
class CloudflareZoneAdmin(BaseAdminMixin):
    """
    Admin configuration for CloudflareZone model.

    Provides admin interface for CloudflareZone model with synchronization
    capabilities for pulling zone data and DNS records from Cloudflare.
    """

    # List display, filter and search
    list_display = ("name", "zone_id", "status")
    list_filter = ("status",)
    search_fields = ("name", "zone_id")

    # Forms
    readonly_fields = ("zone_id",)
    fieldsets = (
        (
            "Zone Details",
            {
                "fields": ("zone_id", "name", "status"),
            },
        ),
    )

    # Actions
    actions_list = [
        {
            "title": "Sync Actions",
            "items": ["pull_all_zones"],
        }
    ]
    actions = ["bulk_pull_zones", "bulk_pull_dns_records"]
    actions_row = ["pull_zone", "pull_dns_records"]
    actions_detail = [
        {
            "title": "Sync Actions",
            "items": ["pull_zone", "pull_dns_records"],
        }
    ]

    # Action Definitions
    @action(
        description="Pull All Zones",
        url_path="pull-all-zones",
        permissions=["pull_all_zones"],
    )
    def pull_all_zones(self, request: HttpRequest):
        """
        Handle pull all zones and DNS records.

        Pulls all zones and their DNS records from Cloudflare.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirect to the zone list page.
        """
        try:
            sync_cloudflare_zones.delay()
            self.message_user(
                request,
                "Queued Zone Sync",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarezone_changelist"))

    @admin.action(description="Pull zone data from Cloudflare")
    def bulk_pull_zones(self, request: HttpRequest, queryset: QuerySet[CloudflareZone]):
        """
        Bulk action to pull zone data from multiple zones.

        Pulls zone data from Cloudflare for all selected zones in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected zone objects to pull data for.
        """
        try:
            for record in queryset:
                sync_cloudflare_zone.delay(db_id=record.id)

            self.message_user(
                request,
                "Queued Zone Pulls",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error: {str(e)}",
                level=messages.ERROR,
            )

    @admin.action(description="Pull DNS records from Cloudflare")
    def bulk_pull_dns_records(self, request: HttpRequest, queryset):
        """
        Bulk action to pull DNS records from multiple zones.

        Pulls DNS records from Cloudflare for all selected zones in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected zone objects to pull DNS records for.
        """
        try:
            for record in queryset:
                sync_cloudflare_zone_dns_records.delay(db_id=record.id)

            self.message_user(
                request,
                "Queued Zone Pulls",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error: {str(e)}",
                level=messages.ERROR,
            )

    @action(
        description="Pull Zone",
        url_path="pull-zone",
        permissions=["pull_zone"],
    )
    def pull_zone(self, request: HttpRequest, object_id: int):
        """
        Handle pull action for a single zone.

        Pulls zone data from Cloudflare for a specific zone instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The primary key of the zone to pull.

        Returns:
            HttpResponseRedirect: Redirect to the zone detail page.
        """
        zone = self.get_object(request, object_id)
        if zone is None:
            self.message_user(request, "Zone not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarezone_changelist"))

        try:
            zone.pull()
            self.message_user(
                request,
                f"Successfully pulled zone data for {zone.name}. Status: {zone.status}",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error pulling zone data for {zone.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarezone_change", args=[object_id])
        )

    @action(
        description="Pull DNS Records",
        url_path="pull-dns-records",
        permissions=["pull_dns_records"],
    )
    def pull_dns_records(self, request: HttpRequest, object_id: int):
        """
        Handle pull DNS records action for a single zone.

        Pulls DNS records from Cloudflare for a specific zone instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The primary key of the zone to pull DNS records for.

        Returns:
            HttpResponseRedirect: Redirect to the zone detail page.
        """
        zone = self.get_object(request, object_id)
        if zone is None:
            self.message_user(request, "Zone not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarezone_changelist"))

        try:
            zone.pull_dns_records()
            self.message_user(
                request,
                f"Successfully pulled DNS records for {zone.name}.",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error pulling DNS records for {zone.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarezone_change", args=[object_id])
        )

    # Permission Checks
    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disable adding new zones via admin - zones should only be added via pull."""
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: CloudflareZone | None = None
    ) -> bool:
        """Disable changing zones via admin - zones should only be updated via pull."""
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: CloudflareZone | None = None
    ) -> bool:
        """Disable deleting zones via admin - zones are read-only."""
        return False

    def has_pull_zone_permission(
        self, _request: HttpRequest, _obj: CloudflareZone | None = None
    ) -> bool:
        """Check if user has permission to pull zone.

        Args:
            _request: The HTTP request object.
            _obj: The CloudflareZone instance (None for list view).

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return True

    def has_pull_dns_records_permission(
        self, _request: HttpRequest, _obj: CloudflareZone | None = None
    ) -> bool:
        """Check if user has permission to pull DNS records.

        Args:
            _request: The HTTP request object.
            _obj: The CloudflareZone instance (None for list view).

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return True

    def has_pull_all_zones_permission(self, _request: HttpRequest) -> bool:
        """Check if user has permission to pull all zones.

        Args:
            _request: The HTTP request object.

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return True


@admin.register(CloudflareDNSRecord)
class CloudflareDNSRecordAdmin(BaseAdminMixin):
    """
    Admin configuration for CloudflareDNSRecord model.

    Provides admin interface for CloudflareDNSRecord model with synchronization
    capabilities for pulling and pushing DNS records to/from Cloudflare.
    """

    # List display, filter and search
    list_display = ("name", "dns_type", "content", "proxied", "zone")
    list_filter = ("dns_type", "proxied", "zone")
    search_fields = ("name", "content", "dns_id")

    # Forms
    readonly_fields = ("dns_id", "zone", "proxiable")
    fieldsets = (
        (
            "DNS Record Details",
            {
                "fields": ("dns_id", "name", "dns_type", "content", "zone"),
            },
        ),
        (
            "Proxy & TTL Settings",
            {
                "fields": ("proxiable", "proxied", "ttl", "auto_ttl"),
            },
        ),
        (
            "Additional Information",
            {
                "fields": ("comment",),
            },
        ),
    )
