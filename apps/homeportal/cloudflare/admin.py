"""Admin config for the Cloudflare app."""

from logging import getLogger

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from unfold.decorators import action

from cloudflare.models import CloudflareDNSRecord, CloudflareZone
from cloudflare.tasks import (
    pull_all_dns_records,
    pull_dns_record,
    push_all_dns_records,
    push_dns_record,
    sync_cloudflare_zone,
    sync_cloudflare_zone_dns_records,
    sync_cloudflare_zones,
)
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
    def pull_all_zones(self, request: HttpRequest) -> None:
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
    def bulk_pull_zones(self, request: HttpRequest, queryset: QuerySet[CloudflareZone]) -> None:
        """
        Bulk action to pull zone data from multiple zones.

        Pulls zone data from Cloudflare for all selected zones in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected zone objects to pull data for.
        """
        try:
            user = request.user

            records: list[CloudflareZone] = []
            skipped = 0

            for record in queryset:
                if user.has_perm("cloudflare.pull_zone", record):
                    records.append(record)
                else:
                    skipped += 1

            if skipped:
                self.message_user(
                    request,
                    f"Skipped {skipped} zone pulls due to insufficient permissions.",
                    level=messages.WARNING,
                )

            for record in records:
                sync_cloudflare_zone.delay(db_id=record.id)

            self.message_user(
                request,
                f"Queued Zone Pulls (Count: ({len(records)}))",
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
    def bulk_pull_dns_records(self, request: HttpRequest, queryset) -> None:
        """
        Bulk action to pull DNS records from multiple zones.

        Pulls DNS records from Cloudflare for all selected zones in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected zone objects to pull DNS records for.
        """
        try:
            user = request.user

            records: list[CloudflareZone] = []
            skipped = 0

            for record in queryset:
                if user.has_perm("cloudflare.pull_zone_dns", record):
                    records.append(record)
                else:
                    skipped += 1

            if skipped:
                self.message_user(
                    request,
                    f"Skipped {skipped} zone pulls due to insufficient permissions.",
                    level=messages.WARNING,
                )

            for record in records:
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
    def pull_zone(self, request: HttpRequest, object_id: int) -> HttpResponseRedirect:
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
    def pull_dns_records(self, request: HttpRequest, object_id: int) -> HttpResponseRedirect:
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
        self, request: HttpRequest, obj: CloudflareZone | None = None
    ) -> bool:
        """Check if user has permission to pull zone.

        Args:
            request: The HTTP request object.
            obj: The CloudflareZone instance (None for list view).

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return request.user.has_perm("cloudflare.pull_zone", obj)

    def has_pull_dns_records_permission(
        self, request: HttpRequest, obj: CloudflareZone | None = None
    ) -> bool:
        """Check if user has permission to pull DNS records.

        Args:
            request: The HTTP request object.
            obj: The CloudflareZone instance (None for list view).

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return request.user.has_perm("cloudflare.pull_zone_dns", obj)

    def has_pull_all_zones_permission(self, request: HttpRequest) -> bool:
        """Check if user has permission to pull all zones.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return request.user.is_superuser


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
    readonly_fields = ("dns_id", "proxiable")
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

    # Actions
    actions_list = [
        {
            "title": "Sync Actions",
            "items": ["pull_all_records", "push_all_records"],
        }
    ]
    actions = ["bulk_pull_dns_records", "bulk_push_dns_records"]
    actions_row = ["pull_record", "push_record"]
    actions_detail = [
        {
            "title": "Sync Actions",
            "items": ["pull_record", "push_record"],
        }
    ]
    actions_submit_line = ["save_and_push"]

    # Utils
    def delete_queryset(
        self, request: HttpRequest, queryset: QuerySet[CloudflareDNSRecord]
    ) -> None:
        """
        Override bulk delete to call each record's delete method.

        This ensures that DNS records are deleted from Cloudflare via the API
        before being removed from the database, as the model's custom delete()
        method handles the Cloudflare API deletion.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected DNS records to delete.
        """
        try:
            user = request.user

            records: list[CloudflareDNSRecord] = []
            skipped = 0

            for record in queryset:
                if user.has_perm("cloudflare.delete", record):
                    records.append(record)
                else:
                    skipped += 1

            if skipped:
                self.message_user(
                    request,
                    f"Skipped {skipped} DNS record deletions due to insufficient permissions.",
                    level=messages.WARNING,
                )

            for record in records:
                record.delete()

            self.message_user(
                request,
                f"Successfully deleted {len(records)} DNS records from Cloudflare and database.",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception during bulk delete: {e}")
            self.message_user(
                request,
                f"Error during bulk delete: {str(e)}",
                level=messages.ERROR,
            )

    def get_readonly_fields(
        self, request: HttpRequest, obj: CloudflareDNSRecord | None = None
    ) -> tuple[str]:
        """
        Make zone field readonly after creation.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (CloudflareDNSRecord | None): The DNS record instance being edited (None for add).

        Returns:
            tuple: Tuple of readonly field names.
        """
        readonly = list(super().get_readonly_fields(request, obj))

        if obj is not None:
            readonly.append("zone")

        return tuple(readonly)

    # Action Definitions
    @action(
        description="Pull All DNS Records",
        url_path="pull-all-records",
        permissions=["pull_all_records"],
    )
    def pull_all_records(self, request: HttpRequest) -> HttpResponseRedirect:
        """
        Handle pull all DNS records action.

        Pulls all DNS records from Cloudflare across all zones.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirect to the DNS record list page.
        """
        try:
            pull_all_dns_records.delay()
            self.message_user(
                request,
                "Queued Pull All DNS Records",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarednsrecord_changelist"))

    @action(
        description="Push All DNS Records",
        url_path="push-all-records",
        permissions=["push_all_records"],
    )
    def push_all_records(self, request: HttpRequest) -> HttpResponseRedirect:
        """
        Handle push all DNS records action.

        Pushes all DNS records to Cloudflare.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirect to the DNS record list page.
        """
        try:
            push_all_dns_records.delay()
            self.message_user(
                request,
                "Queued Push All DNS Records",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarednsrecord_changelist"))

    @admin.action(description="Pull DNS records from Cloudflare")
    def bulk_pull_dns_records(
        self, request: HttpRequest, queryset: QuerySet[CloudflareDNSRecord]
    ) -> None:
        """
        Bulk action to pull DNS records from Cloudflare.

        Pulls DNS record data from Cloudflare for all selected DNS records in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected DNS record objects to pull data for.
        """
        try:
            user = request.user

            records: list[CloudflareDNSRecord] = []
            skipped = 0

            for record in queryset:
                if user.has_perm("cloudflare.pull", record):
                    records.append(record)
                else:
                    skipped += 1

            if skipped:
                self.message_user(
                    request,
                    f"Skipped {skipped} DNS record pulls due to insufficient permissions.",
                    level=messages.WARNING,
                )

            for record in records:
                pull_dns_record.delay(db_id=record.id)

            self.message_user(
                request,
                f"Queued DNS Record Pulls (Count: {len(records)})",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error: {str(e)}",
                level=messages.ERROR,
            )

    @admin.action(description="Push DNS records to Cloudflare")
    def bulk_push_dns_records(
        self, request: HttpRequest, queryset: QuerySet[CloudflareDNSRecord]
    ) -> None:
        """
        Bulk action to push DNS records to Cloudflare.

        Pushes DNS record data to Cloudflare for all selected DNS records in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected DNS record objects to push data for.
        """
        try:
            user = request.user

            records: list[CloudflareDNSRecord] = []
            skipped = 0

            for record in queryset:
                if user.has_perm("cloudflare.push", record):
                    records.append(record)
                else:
                    skipped += 1

            if skipped:
                self.message_user(
                    request,
                    f"Skipped {skipped} DNS record pushes due to insufficient permissions.",
                    level=messages.WARNING,
                )

            for record in records:
                push_dns_record.delay(db_id=record.id)

            self.message_user(
                request,
                f"Queued DNS Record Pushes (Count: {len(records)})",
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
        description="Pull DNS Record",
        url_path="pull-record",
        permissions=["pull_record"],
    )
    def pull_record(self, request: HttpRequest, object_id: int) -> HttpResponseRedirect:
        """
        Handle pull action for a single DNS record.

        Pulls DNS record data from Cloudflare for a specific DNS record instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The primary key of the DNS record to pull.

        Returns:
            HttpResponseRedirect: Redirect to the DNS record detail page.
        """
        dns_record = self.get_object(request, object_id)
        if dns_record is None:
            self.message_user(request, "DNS Record not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarednsrecord_changelist"))

        try:
            dns_record.pull()
            self.message_user(
                request,
                f"Successfully pulled DNS record data for {dns_record.name}.",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error pulling DNS record data for {dns_record.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarednsrecord_change", args=[object_id])
        )

    @action(
        description="Push DNS Record",
        url_path="push-record",
        permissions=["push_record"],
    )
    def push_record(self, request: HttpRequest, object_id: int) -> HttpResponseRedirect:
        """
        Handle push action for a single DNS record.

        Pushes DNS record data to Cloudflare for a specific DNS record instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The primary key of the DNS record to push.

        Returns:
            HttpResponseRedirect: Redirect to the DNS record detail page.
        """
        dns_record = self.get_object(request, object_id)
        if dns_record is None:
            self.message_user(request, "DNS Record not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarednsrecord_changelist"))

        try:
            dns_record.push()
            self.message_user(
                request,
                f"Successfully pushed DNS record data for {dns_record.name}.",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Error pushing DNS record data for {dns_record.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarednsrecord_change", args=[object_id])
        )

    @action(
        description="Save & Push",
        permissions=["save_and_push"],
    )
    def save_and_push(self, request: HttpRequest, obj: CloudflareDNSRecord):
        """
        Submit line action to save and push DNS record to Cloudflare.

        This action is triggered after the form is saved. It pushes the saved
        DNS record data to Cloudflare.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (CloudflareDNSRecord): The saved DNS record instance.
        """
        try:
            obj.push()
            self.message_user(
                request,
                f"Successfully saved and pushed DNS record {obj.name} to Cloudflare.",
                level=messages.SUCCESS,
            )
        except Exception as e:
            log.error(f"Exception: {e}")
            self.message_user(
                request,
                f"Saved locally but failed to push to Cloudflare: {str(e)}",
                level=messages.ERROR,
            )

    # Permission Checks
    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disable adding new zones via admin - zones should only be added via pull."""
        return request.user.has_perm("cloudflare.add_cloudflarednsrecord")

    def has_change_permission(
        self, request: HttpRequest, obj: CloudflareZone | None = None
    ) -> bool:
        """Disable changing zones via admin - zones should only be updated via pull."""
        return request.user.has_perm("cloudflare.update", obj)

    def has_delete_permission(
        self, request: HttpRequest, obj: CloudflareZone | None = None
    ) -> bool:
        """Disable deleting zones via admin - zones are read-only."""
        return request.user.has_perm("cloudflare.delete", obj)

    def has_pull_record_permission(
        self, request: HttpRequest, obj: CloudflareDNSRecord | None = None
    ) -> bool:
        """Check if user has permission to pull a DNS record.

        Args:
            request: The HTTP request object.
            obj: The CloudflareDNSRecord instance (None for list view).

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return request.user.has_perm("cloudflare.pull", obj)

    def has_push_record_permission(
        self, request: HttpRequest, obj: CloudflareDNSRecord | None = None
    ) -> bool:
        """Check if user has permission to push a DNS record.

        Args:
            request: The HTTP request object.
            obj: The CloudflareDNSRecord instance (None for list view).

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return request.user.has_perm("cloudflare.push", obj)

    def has_pull_all_records_permission(self, request: HttpRequest) -> bool:
        """Check if user has permission to pull all DNS records.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return request.user.is_superuser

    def has_push_all_records_permission(self, request: HttpRequest) -> bool:
        """Check if user has permission to push all DNS records.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True if user has permission, False otherwise.
        """
        return request.user.is_superuser

    def has_save_and_push_permission(self, request: HttpRequest, object_id: str | int) -> bool:
        """Check if user has permission to save and push a DNS record.

        Args:
            request: The HTTP request object.
            object_id: The ID of the DNS record being edited.

        Returns:
            bool: True if user has permission, False otherwise.
        """
        record = CloudflareDNSRecord.objects.get(id=object_id)
        return request.user.has_perm("cloudflare.push", record)
