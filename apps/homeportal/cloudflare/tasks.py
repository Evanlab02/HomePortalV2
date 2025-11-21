"""Contains celery tasks for cloudflare app."""

from logging import getLogger
from typing import Any

from celery import Task, shared_task
from requests import HTTPError

from app.schemas import CeleryMetaData
from cloudflare.models import CloudflareDNSRecord, CloudflareZone

logger = getLogger(__name__)


@shared_task(bind=True)
def sync_cloudflare_zones(self: Task) -> dict[str, Any]:
    """
    Synchronize all Cloudflare zones and DNS records.

    Fetches all zones from the Cloudflare API and syncs them with the local database.
    This includes creating new zones, updating existing zones, deleting removed zones,
    and pulling DNS records for all zones.

    Returns:
        dict[str, Any]: Metadata about the task execution including total zones and DNS records
            synced.
    """
    metadata = CeleryMetaData(task="Sync Cloudflare Zones", indeterminate=True)
    metadata.propagate(self)
    logger.info("Starting Cloudflare Zones Sync...")

    try:
        CloudflareZone.pull_all()
        zone_count = CloudflareZone.objects.all().count()
        dns_count = CloudflareDNSRecord.objects.all().count()
        metadata.result = {"Total Zones": zone_count, "Total DNS Records": dns_count}
    except HTTPError as e:
        logger.error(f"Zone Sync HTTP Req Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.propagate(self)
        raise e

    logger.info("Completed Cloudflare zones sync.")
    return metadata.model_dump()


@shared_task(bind=True)
def sync_cloudflare_zone(self: Task, db_id: int) -> dict[str, Any]:
    """
    Synchronize a single Cloudflare zone.

    Fetches the latest zone data from Cloudflare API for a specific zone
    and updates the local database.

    Args:
        self (Task): The Celery task instance.
        db_id (int): The database ID of the Cloudflare zone to sync.

    Returns:
        dict[str, Any]: Metadata about the task execution.

    Raises:
        CloudflareZone.DoesNotExist: If the zone doesn't exist in the database.
        HTTPError: If the Cloudflare API request fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(
        task="Sync Cloudflare Zone",
        indeterminate=True,
        result={"db_id": db_id},
    )
    metadata.propagate(self)
    logger.info(f"Starting Cloudflare Zone Sync... (DB_ID: {db_id})")

    try:
        zone = CloudflareZone.objects.get(id=db_id)
        zone.pull()
    except CloudflareZone.DoesNotExist as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "Record Does Not Exist"
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.propagate(self)
        raise e

    logger.info(f"Completed Cloudflare zone sync. (DB_ID: {db_id})")
    return metadata.model_dump()


@shared_task(bind=True)
def sync_cloudflare_zone_dns_records(self: Task, db_id: int) -> dict[str, Any]:
    """
    Synchronize DNS records for a specific Cloudflare zone.

    Fetches all DNS records from Cloudflare API for a specific zone
    and updates the local database.

    Args:
        self (Task): The Celery task instance.
        db_id (int): The database ID of the Cloudflare zone whose DNS records should be synced.

    Returns:
        dict[str, Any]: Metadata about the task execution.

    Raises:
        CloudflareZone.DoesNotExist: If the zone doesn't exist in the database.
        HTTPError: If the Cloudflare API request fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(
        task="Sync Cloudflare Zone DNS", indeterminate=True, result={"db_id": db_id}
    )
    metadata.propagate(self)
    logger.info(f"Starting Cloudflare Zone DNS Sync... (DB_ID: {db_id})")

    try:
        zone = CloudflareZone.objects.get(id=db_id)
        zone.pull_dns_records()
    except CloudflareZone.DoesNotExist as e:
        logger.error(f"Zone DNS Sync Failed: {e}")
        metadata.state = "Record Does Not Exist"
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"Zone DNS Sync Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Zone DNS Sync Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.propagate(self)
        raise e

    logger.info(f"Completed Cloudflare Zone DNS Sync. (DB_ID: {db_id})")
    return metadata.model_dump()


@shared_task(bind=True)
def pull_dns_record(self: Task, db_id: int) -> dict[str, Any]:
    """
    Pull a single DNS record from Cloudflare API.

    Fetches the latest data from Cloudflare API for a specific DNS record
    and updates the local database.

    Args:
        self (Task): The Celery task instance.
        db_id (int): The database ID of the DNS record to pull.

    Returns:
        dict[str, Any]: Metadata about the task execution.

    Raises:
        CloudflareDNSRecord.DoesNotExist: If the DNS record doesn't exist in the database.
        HTTPError: If the Cloudflare API request fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Pull DNS Record", result={"db_id": db_id})
    metadata.propagate(self)
    logger.info(f"Starting DNS Record Pull... (DB_ID: {db_id})")

    try:
        metadata.state = "Getting DNS Record..."
        metadata.current = 20
        metadata.propagate(self)
        dns_record = CloudflareDNSRecord.objects.get(id=db_id)

        metadata.state = "Pulling DNS Record..."
        metadata.current = 80
        metadata.propagate(self)
        dns_record.pull()

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.propagate(self)
    except CloudflareDNSRecord.DoesNotExist as e:
        logger.error(f"DNS Record Pull Failed: {e}")
        metadata.state = "Record Does Not Exist"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"DNS Record Pull Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"DNS Record Pull Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info(f"Completed DNS Record Pull. (DB_ID: {db_id})")
    return metadata.model_dump()


@shared_task(bind=True)
def push_dns_record(self: Task, db_id: int) -> dict[str, Any]:
    """
    Push a single DNS record to Cloudflare API.

    Pushes local changes to Cloudflare API for a specific DNS record.

    Args:
        self (Task): The Celery task instance.
        db_id (int): The database ID of the DNS record to push.

    Returns:
        dict[str, Any]: Metadata about the task execution.

    Raises:
        CloudflareDNSRecord.DoesNotExist: If the DNS record doesn't exist in the database.
        HTTPError: If the Cloudflare API request fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Push DNS Record", result={"db_id": db_id})
    metadata.propagate(self)
    logger.info(f"Starting DNS Record Push... (DB_ID: {db_id})")

    try:
        metadata.state = "Getting DNS Record..."
        metadata.current = 20
        metadata.propagate(self)
        dns_record = CloudflareDNSRecord.objects.get(id=db_id)

        metadata.state = "Pushing DNS Record..."
        metadata.current = 80
        metadata.propagate(self)
        dns_record.push()

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.propagate(self)
    except CloudflareDNSRecord.DoesNotExist as e:
        logger.error(f"DNS Record Push Failed: {e}")
        metadata.state = "Record Does Not Exist"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"DNS Record Push Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"DNS Record Push Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info(f"Completed DNS Record Push. (DB_ID: {db_id})")
    return metadata.model_dump()


@shared_task(bind=True)
def pull_all_dns_records(self: Task) -> dict[str, Any]:
    """
    Pull all DNS records from Cloudflare API.

    Fetches all DNS records across all zones from Cloudflare API
    and updates the local database.

    Args:
        self (Task): The Celery task instance.

    Returns:
        dict[str, Any]: Metadata about the task execution including total records pulled.

    Raises:
        HTTPError: If the Cloudflare API request fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Pull All DNS Records")
    metadata.propagate(self)
    logger.info("Starting Pull All DNS Records...")

    try:
        metadata.state = "Getting Zones..."
        metadata.current = 20
        metadata.propagate(self)
        zones = CloudflareZone.objects.all()

        metadata.state = "Pulling DNS Records..."
        metadata.current = 40
        metadata.propagate(self)

        for zone in zones:
            zone.pull_dns_records()

        metadata.state = "Finalizing Results"
        metadata.current = 90
        metadata.propagate(self)
        dns_count = CloudflareDNSRecord.objects.all().count()

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result = {"Total DNS Records": dns_count}
        metadata.propagate(self)
    except HTTPError as e:
        logger.error(f"Pull All DNS Records HTTP Req Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Pull All DNS Records Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info("Completed Pull All DNS Records.")
    return metadata.model_dump()


@shared_task(bind=True)
def push_all_dns_records(self: Task) -> dict[str, Any]:
    """
    Push all DNS records to Cloudflare API.

    Pushes all local DNS records to Cloudflare API, updating
    them with the local changes.

    Args:
        self (Task): The Celery task instance.

    Returns:
        dict[str, Any]: Metadata about the task execution including total records pushed.

    Raises:
        HTTPError: If the Cloudflare API request fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Push All DNS Records")
    metadata.propagate(self)
    logger.info("Starting Push All DNS Records...")

    try:
        metadata.state = "Getting DNS Records..."
        metadata.current = 20
        metadata.propagate(self)
        dns_records = CloudflareDNSRecord.objects.all()

        metadata.state = "Pushing DNS Records..."
        metadata.current = 40
        metadata.propagate(self)

        pushed_count = 0
        for dns_record in dns_records:
            dns_record.push()
            pushed_count += 1

        metadata.state = "Finalizing Results"
        metadata.current = 90
        metadata.propagate(self)

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result = {"Total DNS Records Pushed": pushed_count}
        metadata.propagate(self)
    except HTTPError as e:
        logger.error(f"Push All DNS Records HTTP Req Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Push All DNS Records Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info("Completed Push All DNS Records.")
    return metadata.model_dump()
