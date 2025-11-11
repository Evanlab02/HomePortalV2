"""Contains models for the Cloudflare app."""

from logging import getLogger

from constance import config
from django.db import transaction
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    CheckConstraint,
    ForeignKey,
    IntegerField,
    Q,
    TextField,
)
from requests import Session

from cloudflare.constants import (
    CLOUDFLARE_DNS_RECORDS_CREATE_URL,
    CLOUDFLARE_DNS_RECORDS_DELETE_URL,
    CLOUDFLARE_DNS_RECORDS_DETAIL_URL,
    CLOUDFLARE_DNS_RECORDS_LIST_URL,
    CLOUDFLARE_DNS_RECORDS_UPDATE_URL,
    CLOUDFLARE_ZONES_DETAIL_URL,
    CLOUDFLARE_ZONES_LIST_URL,
)
from cloudflare.schemas import (
    CloudflareDNSRecordIntegrationWrapper,
    CloudflareDNSRecordsIntegrationWrapper,
    CloudflareZoneIntegrationWrapper,
    CloudflareZonesIntegrationWrapper,
)
from utils.models import BaseModel

log = getLogger(__name__)


class CloudflareZone(BaseModel):
    """Model for managing cloudflare zones.

    This model represents a Cloudflare DNS zone and provides methods
    to sync zone data and DNS records between the local database and
    the Cloudflare API.

    Attributes:
        zone_id (str): Unique Cloudflare zone identifier.
        status (str): Current status of the zone (e.g., 'active', 'pending').
        name (str): Domain name associated with the zone.
    """

    zone_id = CharField(unique=True, max_length=50)
    status = CharField(max_length=30)
    name = CharField(max_length=30)

    class Meta:
        """Meta configuration."""

        verbose_name = "Cloudflare Zone"
        verbose_name_plural = "Cloudflare Zones"

    def __str__(self) -> str:
        """Return string representation of the zone."""
        return f"{self.name} ({self.status})"

    def pull(self) -> None:
        """Sync this zone's data from the Cloudflare API.

        Fetches this specific zone's details from the Cloudflare API using
        the zone detail endpoint and updates this zone's status and name
        fields with the latest data from the API. Also triggers a pull of
        all DNS records associated with this zone.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        with Session() as session:
            url = CLOUDFLARE_ZONES_DETAIL_URL.format(zone=self.zone_id)
            response = session.get(
                url=url,
                headers={"Authorization": f"Bearer {config.CLOUDFLARE_API_KEY}"},
            )
            response.raise_for_status()
            data = CloudflareZoneIntegrationWrapper(**response.json())
            results = data.result

        for result in results:
            if result.id != self.zone_id:
                continue

            self.status = result.status
            self.name = result.name
            self.save(update_fields=["status", "name"])
            break

        self.pull_dns_records()
        log.info(f"Completed pull for Cloudflare Zone {self.id} ({self.zone_id})")

    def pull_dns_records(self) -> None:
        """Sync DNS records for this zone from the Cloudflare API.

        Fetches all DNS records for this zone from the Cloudflare API and
        syncs them with the local database by creating new records, updating
        existing ones, and deleting records that no longer exist in the API.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        with Session() as session:
            url = CLOUDFLARE_DNS_RECORDS_LIST_URL.format(zone=self.zone_id)
            response = session.get(
                url=url,
                headers={"Authorization": f"Bearer {config.CLOUDFLARE_API_KEY}"},
            )
            response.raise_for_status()
            data = CloudflareDNSRecordsIntegrationWrapper(**response.json())
            results = data.result

        api_ids = [result.id for result in results]
        api_results_by_id = {result.id: result for result in results}

        dns_records = CloudflareDNSRecord.objects.filter(zone=self)
        existing_dns_record_ids = {dns.dns_id for dns in dns_records}
        dns_records_to_create: list[CloudflareDNSRecord] = []
        dns_records_to_update: list[CloudflareDNSRecord] = []
        dns_records_to_delete: list[CloudflareDNSRecord] = []

        for dns_record in dns_records:
            if dns_record.dns_id in api_ids:
                result = api_results_by_id[dns_record.dns_id]
                dns_record.name = result.name
                dns_record.dns_type = result.dns_type
                dns_record.content = result.content
                dns_record.proxiable = result.proxiable
                dns_record.proxied = result.proxied
                dns_record.comment = result.comment
                dns_record.zone = self

                ttl = result.ttl
                if result.ttl == 1:
                    dns_record.ttl = None
                    dns_record.auto_ttl = True
                else:
                    dns_record.ttl = ttl
                    dns_record.auto_ttl = False

                dns_records_to_update.append(dns_record)
            else:
                dns_records_to_delete.append(dns_record)

        for result in results:
            if result.id not in existing_dns_record_ids:
                dns_records_to_create.append(
                    CloudflareDNSRecord(
                        dns_id=result.id,
                        name=result.name,
                        dns_type=result.dns_type,
                        content=result.content,
                        proxiable=result.proxiable,
                        proxied=result.proxied,
                        ttl=None if result.ttl == 1 else result.ttl,
                        auto_ttl=True if result.ttl == 1 else False,
                        zone=self,
                    )
                )

        with transaction.atomic():
            created_dns_records = CloudflareDNSRecord.objects.bulk_create(dns_records_to_create)
            updated_dns_records_count = CloudflareDNSRecord.objects.bulk_update(
                dns_records_to_update,
                fields=[
                    "name",
                    "dns_type",
                    "content",
                    "proxiable",
                    "proxied",
                    "zone",
                    "ttl",
                    "auto_ttl",
                ],
            )
            deleted_dns_records_count = 0
            if dns_records_to_delete:
                deleted_dns_records_count, _ = CloudflareDNSRecord.objects.filter(
                    id__in=[zone.id for zone in dns_records_to_delete]
                ).delete()

            log.info(f"Created {len(created_dns_records)} DNS records for Zone #{self.zone_id}.")
            log.info(f"Updated {updated_dns_records_count} DNS records Zone #{self.zone_id}.")
            log.info(f"Deleted {deleted_dns_records_count} DNS records Zone #{self.zone_id}.")

    @staticmethod
    def pull_all() -> None:
        """Sync all Cloudflare zones from API to local database.

        Fetches all zones from Cloudflare API and syncs with the local database
        by creating new zones that don't exist locally, updating existing zones
        with latest data, and deleting zones that no longer exist in the API.
        After syncing zones, pulls all DNS records for each zone.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        with Session() as session:
            response = session.get(
                CLOUDFLARE_ZONES_LIST_URL,
                headers={"Authorization": f"Bearer {config.CLOUDFLARE_API_KEY}"},
            )
            response.raise_for_status()
            data = CloudflareZonesIntegrationWrapper(**response.json())
            records = data.result

        api_ids = {record.id for record in records}
        records_by_id = {record.id: record for record in records}

        zones = list(CloudflareZone.objects.all())
        existing_zone_ids = {zone.zone_id for zone in zones}
        zones_to_create: list[CloudflareZone] = []
        zones_to_update: list[CloudflareZone] = []
        zones_to_delete: list[CloudflareZone] = []

        for zone in zones:
            if zone.zone_id in api_ids:
                record = records_by_id[zone.zone_id]
                zone.status = record.status
                zone.name = record.name
                zones_to_update.append(zone)
            else:
                zones_to_delete.append(zone)

        for record in records:
            if record.id not in existing_zone_ids:
                zones_to_create.append(
                    CloudflareZone(
                        zone_id=record.id,
                        status=record.status,
                        name=record.name,
                    )
                )

        with transaction.atomic():
            created_zones = CloudflareZone.objects.bulk_create(zones_to_create)
            updated_zones_count = CloudflareZone.objects.bulk_update(
                zones_to_update, fields=["status", "name"]
            )
            deleted_zones_count = 0
            if zones_to_delete:
                deleted_zones_count, _ = CloudflareZone.objects.filter(
                    id__in=[zone.id for zone in zones_to_delete]
                ).delete()

            log.info(f"Created {len(created_zones)} zones.")
            log.info(f"Updated {updated_zones_count} zones.")
            log.info(f"Deleted {deleted_zones_count} zones.")

        zones = CloudflareZone.objects.all()
        for zone in zones:
            zone.pull_dns_records()


class CloudflareDNSRecord(BaseModel):
    """Model for managing Cloudflare DNS Records.

    This model represents a DNS record in a Cloudflare zone and provides
    methods to create, read, update, and delete DNS records through the
    Cloudflare API.

    Attributes:
        dns_id (str): Unique Cloudflare DNS record identifier.
        name (str): DNS record name (e.g., subdomain or domain).
        dns_type (str): DNS record type (e.g., A, AAAA, CNAME, MX).
        content (str): DNS record content/value (e.g., IP address, hostname).
        proxiable (bool): Whether the record can be proxied through Cloudflare.
        proxied (bool): Whether the record is proxied through Cloudflare.
        ttl (int): Time to live in seconds (None if auto_ttl is True).
        auto_ttl (bool): Whether to use automatic TTL (Cloudflare managed).
        comment (str): Optional comment describing the DNS record.
        zone (CloudflareZone): The Cloudflare zone this record belongs to.
    """

    DNS_TYPE_CHOICES = [
        ("A", "A"),
        ("AAAA", "AAAA"),
        ("CNAME", "CNAME"),
    ]

    dns_id = CharField(unique=True, max_length=50, blank=True)
    name = CharField(max_length=30)
    dns_type = CharField(max_length=10, choices=DNS_TYPE_CHOICES)
    content = CharField(max_length=30)
    proxiable = BooleanField(default=False)
    proxied = BooleanField(default=False)
    ttl = IntegerField(null=True, blank=True)
    auto_ttl = BooleanField(default=False)
    comment = TextField(null=True, blank=True)
    zone = ForeignKey(to=CloudflareZone, on_delete=CASCADE, related_name="dns_records")

    class Meta:
        """Meta configuration."""

        verbose_name = "Cloudflare DNS Record"
        verbose_name_plural = "Cloudflare DNS Records"

        constraints = [
            CheckConstraint(
                condition=Q(dns_type__in=["A", "AAAA", "CNAME"]),
                name="cloudflare_dns_valid_type",
                violation_error_message="DNS type must be one of: A, AAAA, CNAME",
            ),
            CheckConstraint(
                condition=Q(ttl__isnull=True) | Q(ttl__gte=60, ttl__lte=86400),
                name="cloudflare_dns_ttl_range",
                violation_error_message="TTL must be between 60 and 86400 seconds when set.",
            ),
            CheckConstraint(
                condition=Q(proxiable=True) | Q(proxied=False),
                name="cloudflare_dns_proxied_requires_proxiable",
                violation_error_message="Proxied must be False when the record is not proxiable.",
            ),
            CheckConstraint(
                condition=Q(auto_ttl=True, ttl__isnull=True) | Q(auto_ttl=False, ttl__isnull=False),
                name="cloudflare_dns_auto_ttl_consistency",
                violation_error_message="TTL must be null if auto ttl is enabled.",
            ),
        ]

    def __str__(self) -> str:
        """Return string representation of the DNS record."""
        return f"{self.name} ({self.dns_type}) -> {self.content}"

    def create(self) -> None:
        """Create this DNS record in Cloudflare via the API.

        Sends a POST request to the Cloudflare API to create a new DNS record
        with the current instance's data. Updates the instance's dns_id field
        with the ID returned from the API.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        with Session() as session:
            url = CLOUDFLARE_DNS_RECORDS_CREATE_URL.format(zone=self.zone.zone_id)
            response = session.post(
                url,
                headers={"Authorization": f"Bearer {config.CLOUDFLARE_API_KEY}"},
                json={
                    "name": self.name,
                    "type": self.dns_type,
                    "content": self.content,
                    "proxied": self.proxied,
                    "comment": self.comment,
                    "ttl": 1 if self.auto_ttl else self.ttl,
                },
            )
            response.raise_for_status()
            data = CloudflareDNSRecordIntegrationWrapper(**response.json())
            result = data.result

        self.dns_id = result.id

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        """Save the DNS record to the database.

        Overrides Django's default save method to automatically create the
        DNS record in Cloudflare when saving a new instance (when pk is None).
        For existing instances, performs a normal database save.

        Args:
            force_insert (bool): Force INSERT SQL query.
            force_update (bool): Force UPDATE SQL query.
            using (str): Database alias to use for saving.
            update_fields (list): List of field names to update.

        Returns:
            CloudflareDNSRecord: The saved instance.

        Raises:
            requests.HTTPError: If the Cloudflare API request fails (new records only).
        """
        if self.pk is None or self.id is None:
            self.create()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def delete(self, using=None, keep_parents=False):
        """Delete the DNS record from both Cloudflare and the database.

        Overrides Django's default delete method to first delete the DNS record
        from Cloudflare via the API, then remove it from the local database.

        Args:
            using (str): Database alias to use for deletion.
            keep_parents (bool): Keep parent models in the database.

        Returns:
            tuple: A tuple containing the number of objects deleted and a dictionary
                   with the number of deletions per object type.

        Raises:
            requests.HTTPError: If the Cloudflare API request fails.
        """
        with Session() as session:
            url = CLOUDFLARE_DNS_RECORDS_DELETE_URL.format(
                zone=self.zone.zone_id, dns_record=self.dns_id
            )
            response = session.delete(
                url,
                headers={"Authorization": f"Bearer {config.CLOUDFLARE_API_KEY}"},
            )
            response.raise_for_status()
        return super().delete(using, keep_parents)

    def push(self) -> None:
        """Push local changes to Cloudflare via the API.

        Sends a PATCH request to the Cloudflare API to update the DNS record
        with the current instance's data. This method syncs local changes to
        Cloudflare without modifying the local database.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        with Session() as session:
            url = CLOUDFLARE_DNS_RECORDS_UPDATE_URL.format(
                zone=self.zone.zone_id, dns_record=self.dns_id
            )
            response = session.patch(
                url,
                headers={"Authorization": f"Bearer {config.CLOUDFLARE_API_KEY}"},
                json={
                    "name": self.name,
                    "type": self.dns_type,
                    "content": self.content,
                    "proxied": self.proxied,
                    "comment": self.comment,
                    "ttl": 1 if self.auto_ttl else self.ttl,
                },
            )
            response.raise_for_status()

    def pull(self) -> None:
        """Pull the latest data from Cloudflare and update the local record.

        Fetches the current DNS record data from the Cloudflare API and updates
        this instance's fields with the latest values. Automatically saves the
        updated data to the local database.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        with Session() as session:
            url = CLOUDFLARE_DNS_RECORDS_DETAIL_URL.format(
                zone=self.zone.zone_id, dns_record=self.dns_id
            )
            response = session.get(
                url,
                headers={"Authorization": f"Bearer {config.CLOUDFLARE_API_KEY}"},
            )
            response.raise_for_status()
            data = CloudflareDNSRecordIntegrationWrapper(**response.json())
            result = data.result

        self.name = result.name
        self.dns_type = result.dns_type
        self.content = result.content
        self.proxiable = result.proxiable
        self.proxied = result.proxied
        self.comment = result.comment

        ttl = result.ttl
        if ttl == 1:
            self.ttl = None
            self.auto_ttl = True
        else:
            self.ttl = ttl
            self.auto_ttl = False

        self.save()
