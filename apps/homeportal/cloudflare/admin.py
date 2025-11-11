"""Admin config for the Cloudflare app."""

from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from unfold.decorators import display

from cloudflare.models import CloudflareDNSRecord, CloudflareZone
from utils.admin import BaseAdminMixin


@admin.register(CloudflareZone)
class CloudflareZoneAdmin(BaseAdminMixin):
    """Admin configuration for CloudflareZone model.

    Provides admin interface for CloudflareZone model with synchronization
    capabilities for pulling zone data and DNS records from Cloudflare.
    """

    list_display = ("name", "zone_id", "status", "display_sync_actions")
    list_filter = ("status",)
    search_fields = ("name", "zone_id")
    readonly_fields = ("zone_id", "display_sync_actions_detail")

    fieldsets = (
        (
            "Zone Details",
            {
                "fields": ("zone_id", "name", "status"),
            },
        ),
        (
            "Sync Operations",
            {
                "fields": ("display_sync_actions_detail",),
                "description": (
                    "Use these buttons to synchronize zone data "
                    "between the database and Cloudflare."
                ),
            },
        ),
    )

    def get_urls(self):
        """Add custom URLs for single-instance sync operations.

        Extends the default admin URLs with custom endpoints for pulling zone
        data and DNS records from Cloudflare.

        Returns:
            list: Combined list of custom and default admin URLs.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/pull/",
                self.admin_site.admin_view(self.pull_single_view),
                name="cloudflare_cloudflarezone_pull",
            ),
            path(
                "<path:object_id>/pull-dns/",
                self.admin_site.admin_view(self.pull_dns_single_view),
                name="cloudflare_cloudflarezone_pull_dns",
            ),
            path(
                "pull-all/",
                self.admin_site.admin_view(self.pull_all_view),
                name="cloudflare_cloudflarezone_pull_all",
            ),
        ]
        return custom_urls + urls

    @display(description="Actions", label=True)
    def display_sync_actions(self, obj):
        """Display sync action buttons in list view.

        Renders Pull Zone and Pull DNS action buttons for the list view.

        Args:
            obj (CloudflareZone): The zone instance to display actions for.

        Returns:
            str: HTML formatted action buttons.
        """
        pull_url = reverse("admin:cloudflare_cloudflarezone_pull", args=[obj.pk])
        pull_dns_url = reverse("admin:cloudflare_cloudflarezone_pull_dns", args=[obj.pk])
        return format_html(
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-8 px-3 py-2 mr-2" '
            'href="{}">⬇ Pull Zone</a>'
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-8 px-3 py-2" '
            'href="{}">⬇ Pull DNS</a>',
            pull_url,
            pull_dns_url,
        )

    @display(description="", label=False)
    def display_sync_actions_detail(self, obj):
        """Display sync action buttons in detail view.

        Renders Pull Zone and Pull DNS action buttons for the detail view.

        Args:
            obj (CloudflareZone): The zone instance to display actions for.

        Returns:
            str: HTML formatted action buttons or message if object not saved.
        """
        if not obj.pk:
            return "Save the zone first to enable sync actions."

        pull_url = reverse("admin:cloudflare_cloudflarezone_pull", args=[obj.pk])
        pull_dns_url = reverse("admin:cloudflare_cloudflarezone_pull_dns", args=[obj.pk])
        return format_html(
            '<div class="flex gap-4">'
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2" '
            'href="{}">⬇ Pull Zone from Cloudflare</a>'
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2" '
            'href="{}">⬇ Pull DNS Records from Cloudflare</a>'
            "</div>",
            pull_url,
            pull_dns_url,
        )

    def pull_single_view(self, request: HttpRequest, object_id: str):
        """Handle pull action for a single zone.

        Pulls zone data from Cloudflare for a specific zone instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The primary key of the zone to pull.

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
            self.message_user(
                request,
                f"Error pulling zone data for {zone.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarezone_change", args=[object_id])
        )

    def pull_dns_single_view(self, request: HttpRequest, object_id: str):
        """Handle pull DNS records action for a single zone.

        Pulls DNS records from Cloudflare for a specific zone instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The primary key of the zone to pull DNS records for.

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
            self.message_user(
                request,
                f"Error pulling DNS records for {zone.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarezone_change", args=[object_id])
        )

    def pull_all_view(self, request: HttpRequest):
        """Handle pull all zones and DNS records.

        Pulls all zones and their DNS records from Cloudflare.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirect to the zone list page.
        """
        try:
            CloudflareZone.pull_all()
            self.message_user(
                request,
                "Successfully pulled all zones and DNS records from Cloudflare.",
                level=messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error pulling all zones: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarezone_changelist"))

    @admin.action(description="Pull zone data from Cloudflare")
    def bulk_pull_zones(self, request: HttpRequest, queryset):
        """Bulk action to pull zone data from multiple zones.

        Pulls zone data from Cloudflare for all selected zones in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected zone objects to pull data for.
        """
        success_count = 0
        error_count = 0

        for zone in queryset:
            try:
                zone.pull()
                success_count += 1
            except Exception:
                error_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"Successfully pulled zone data from {success_count} zone(s).",
                level=messages.SUCCESS,
            )

        if error_count > 0:
            self.message_user(
                request,
                f"Failed to pull zone data from {error_count} zone(s).",
                level=messages.ERROR,
            )

    @admin.action(description="Pull DNS records from Cloudflare")
    def bulk_pull_dns_records(self, request: HttpRequest, queryset):
        """Bulk action to pull DNS records from multiple zones.

        Pulls DNS records from Cloudflare for all selected zones in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected zone objects to pull DNS records for.
        """
        success_count = 0
        error_count = 0

        for zone in queryset:
            try:
                zone.pull_dns_records()
                success_count += 1
            except Exception:
                error_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"Successfully pulled DNS records from {success_count} zone(s).",
                level=messages.SUCCESS,
            )

        if error_count > 0:
            self.message_user(
                request,
                f"Failed to pull DNS records from {error_count} zone(s).",
                level=messages.ERROR,
            )

    actions = ["bulk_pull_zones", "bulk_pull_dns_records"]


@admin.register(CloudflareDNSRecord)
class CloudflareDNSRecordAdmin(BaseAdminMixin):
    """Admin configuration for CloudflareDNSRecord model.

    Provides admin interface for CloudflareDNSRecord model with synchronization
    capabilities for pulling and pushing DNS records to/from Cloudflare.
    """

    list_display = ("name", "dns_type", "content", "proxied", "zone", "display_sync_actions")
    list_filter = ("dns_type", "proxied", "zone")
    search_fields = ("name", "content", "dns_id")
    readonly_fields = ("dns_id", "display_sync_actions_detail")

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
        (
            "Sync Operations",
            {
                "fields": ("display_sync_actions_detail",),
                "description": (
                    "Use these buttons to synchronize DNS record data "
                    "between the database and Cloudflare."
                ),
            },
        ),
    )

    def get_urls(self):
        """Add custom URLs for single-instance sync operations.

        Extends the default admin URLs with custom endpoints for pulling and
        pushing DNS records to/from Cloudflare.

        Returns:
            list: Combined list of custom and default admin URLs.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/pull/",
                self.admin_site.admin_view(self.pull_single_view),
                name="cloudflare_cloudflarednsrecord_pull",
            ),
            path(
                "<path:object_id>/push/",
                self.admin_site.admin_view(self.push_single_view),
                name="cloudflare_cloudflarednsrecord_push",
            ),
        ]
        return custom_urls + urls

    @display(description="Actions", label=True)
    def display_sync_actions(self, obj):
        """Display sync action buttons in list view.

        Renders Pull and Push action buttons for the list view.

        Args:
            obj (CloudflareDNSRecord): The DNS record instance to display actions for.

        Returns:
            str: HTML formatted action buttons.
        """
        pull_url = reverse("admin:cloudflare_cloudflarednsrecord_pull", args=[obj.pk])
        push_url = reverse("admin:cloudflare_cloudflarednsrecord_push", args=[obj.pk])
        return format_html(
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-8 px-3 py-2 mr-2" '
            'href="{}">⬇ Pull</a>'
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-8 px-3 py-2" '
            'href="{}">⬆ Push</a>',
            pull_url,
            push_url,
        )

    @display(description="", label=False)
    def display_sync_actions_detail(self, obj):
        """Display sync action buttons in detail view.

        Renders Pull and Push action buttons for the detail view.

        Args:
            obj (CloudflareDNSRecord): The DNS record instance to display actions for.

        Returns:
            str: HTML formatted action buttons or message if object not saved.
        """
        if not obj.pk:
            return "Save the DNS record first to enable sync actions."

        pull_url = reverse("admin:cloudflare_cloudflarednsrecord_pull", args=[obj.pk])
        push_url = reverse("admin:cloudflare_cloudflarednsrecord_push", args=[obj.pk])
        return format_html(
            '<div class="flex gap-4">'
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2" '
            'href="{}">⬇ Pull DNS Record from Cloudflare</a>'
            '<a class="inline-flex items-center justify-center rounded-md text-sm '
            "font-medium ring-offset-background transition-colors "
            "focus-visible:outline-none focus-visible:ring-2 "
            "focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50 bg-primary "
            'text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2" '
            'href="{}">⬆ Push DNS Record to Cloudflare</a>'
            "</div>",
            pull_url,
            push_url,
        )

    def pull_single_view(self, request: HttpRequest, object_id: str):
        """Handle pull action for a single DNS record.

        Pulls DNS record data from Cloudflare for a specific record instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The primary key of the DNS record to pull.

        Returns:
            HttpResponseRedirect: Redirect to the DNS record detail page.
        """
        dns_record = self.get_object(request, object_id)
        if dns_record is None:
            self.message_user(request, "DNS record not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarednsrecord_changelist"))

        try:
            dns_record.pull()
            self.message_user(
                request,
                f"Successfully pulled DNS record {dns_record.name}. Type: {dns_record.dns_type}",
                level=messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error pulling DNS record {dns_record.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarednsrecord_change", args=[object_id])
        )

    def push_single_view(self, request: HttpRequest, object_id: str):
        """Handle push action for a single DNS record.

        Pushes DNS record data to Cloudflare for a specific record instance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The primary key of the DNS record to push.

        Returns:
            HttpResponseRedirect: Redirect to the DNS record detail page.
        """
        dns_record = self.get_object(request, object_id)
        if dns_record is None:
            self.message_user(request, "DNS record not found.", level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:cloudflare_cloudflarednsrecord_changelist"))

        try:
            dns_record.push()
            self.message_user(
                request,
                f"Successfully pushed DNS record {dns_record.name}. Type: {dns_record.dns_type}",
                level=messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error pushing DNS record {dns_record.name}: {str(e)}",
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse("admin:cloudflare_cloudflarednsrecord_change", args=[object_id])
        )

    @admin.action(description="Pull DNS records from Cloudflare")
    def bulk_pull_dns_records(self, request: HttpRequest, queryset):
        """Bulk action to pull DNS records from Cloudflare.

        Pulls DNS record data from Cloudflare for all selected records in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected DNS record objects to pull data for.
        """
        success_count = 0
        error_count = 0

        for dns_record in queryset:
            try:
                dns_record.pull()
                success_count += 1
            except Exception:
                error_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"Successfully pulled {success_count} DNS record(s).",
                level=messages.SUCCESS,
            )

        if error_count > 0:
            self.message_user(
                request,
                f"Failed to pull {error_count} DNS record(s).",
                level=messages.ERROR,
            )

    @admin.action(description="Push DNS records to Cloudflare")
    def bulk_push_dns_records(self, request: HttpRequest, queryset):
        """Bulk action to push DNS records to Cloudflare.

        Pushes DNS record data to Cloudflare for all selected records in the queryset.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The selected DNS record objects to push data for.
        """
        success_count = 0
        error_count = 0

        for dns_record in queryset:
            try:
                dns_record.push()
                success_count += 1
            except Exception:
                error_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"Successfully pushed {success_count} DNS record(s).",
                level=messages.SUCCESS,
            )

        if error_count > 0:
            self.message_user(
                request,
                f"Failed to push {error_count} DNS record(s).",
                level=messages.ERROR,
            )

    actions = ["bulk_pull_dns_records", "bulk_push_dns_records"]
