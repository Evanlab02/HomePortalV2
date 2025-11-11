"""Contains Cloudflare API schemas."""

from pydantic import BaseModel, ConfigDict, Field


class CloudflareZoneIntegration(BaseModel):
    """Cloudflare zone schema for API integration.

    Represents a Cloudflare zone returned from the Cloudflare API.
    Used for parsing zone data including zone ID, name, and status.

    Attributes:
        id (str): The unique zone identifier.
        name (str): The zone name, typically the domain name.
        status (str): The current status of the zone.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="The zone ID.")
    name: str = Field(..., description="The zone name, often the domain name.")
    status: str = Field(..., description="The status of the zone.")


class CloudflareZoneIntegrationWrapper(BaseModel):
    """Cloudflare zone wrapper schema for API integration.

    Wraps a list of Cloudflare zones returned from the Cloudflare API.
    Used for parsing the API response containing multiple zones.

    Attributes:
        result (list[CloudflareZoneIntegration]): List of Cloudflare zones.
    """

    model_config = ConfigDict(extra="ignore")

    result: list[CloudflareZoneIntegration]


class CloudflareDNSRecordIntegration(BaseModel):
    """Cloudflare DNS record schema for API integration.

    Represents a Cloudflare DNS record returned from the Cloudflare API.
    Used for parsing DNS record data including type, content, and proxy settings.

    Attributes:
        id (str): The unique DNS record identifier.
        name (str): The DNS record name.
        dns_type (str): The DNS record type (A, AAAA, CNAME, etc.).
        content (str): The DNS record content/value.
        proxiable (str): Whether the record can be proxied through Cloudflare.
        proxied (str): Whether the record is currently proxied.
        ttl (int): Time to live for the DNS record in seconds.
        comment (str): Optional comment for the DNS record.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="The unique DNS record identifier.")
    name: str = Field(..., description="The DNS record name.")
    dns_type: str = Field(
        ..., description="The DNS record type (A, AAAA, CNAME, etc.).", alias="type"
    )
    content: str = Field(..., description="The DNS record content/value.")
    proxiable: bool = Field(
        ..., description="Whether the record can be proxied through Cloudflare."
    )
    proxied: bool = Field(..., description="Whether the record is currently proxied.")
    ttl: int = Field(..., description="Time to live for the DNS record in seconds.")
    comment: str | None = Field(..., description="Optional comment for the DNS record.")


class CloudflareDNSRecordIntegrationWrapper(BaseModel):
    """Cloudflare DNS record wrapper schema for API integration.

    Wraps a single Cloudflare DNS record returned from the Cloudflare API.
    Used for parsing the API response containing a single DNS record.

    Attributes:
        result (CloudflareDNSRecordIntegration): Single Cloudflare DNS record.
    """

    model_config = ConfigDict(extra="ignore")

    result: CloudflareDNSRecordIntegration


class CloudflareDNSRecordsIntegrationWrapper(BaseModel):
    """Cloudflare DNS records wrapper schema for API integration.

    Wraps a list of Cloudflare DNS records returned from the Cloudflare API.
    Used for parsing the API response containing multiple DNS records.

    Attributes:
        result (list[CloudflareDNSRecordIntegration]): List of Cloudflare DNS records.
    """

    model_config = ConfigDict(extra="ignore")

    result: list[CloudflareDNSRecordIntegration]
