"""Contains celery tasks for cloudflare app."""

from typing import Any
from logging import getLogger

from celery import shared_task, Task
from requests import HTTPError

from app.schemas import CeleryMetaData
from cloudflare.models import CloudflareZone, CloudflareDNSRecord

logger = getLogger(__name__)


@shared_task(bind=True)
def sync_cloudflare_zones(self: Task) -> dict[str, Any]:
    """
    Synchronize all Cloudflare zones and DNS records.

    Fetches all zones from the Cloudflare API and syncs them with the local database.
    This includes creating new zones, updating existing zones, deleting removed zones,
    and pulling DNS records for all zones.

    Returns:
        TODO
    """
    metadata = CeleryMetaData(task="Sync Cloudflare Zones")
    metadata.propagate(self)
    logger.info("Starting Cloudflare Zones Sync...")

    try:
        metadata.state = "Started Zones Sync"
        metadata.current = 40
        metadata.propagate(self)
        CloudflareZone.pull_all()

        metadata.state = "Finalizing Results"
        metadata.current = 90
        metadata.propagate(self)
        zone_count = CloudflareZone.objects.all().count()
        dns_count = CloudflareDNSRecord.objects.all().count()

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result = {"Total Zones": zone_count, "Total DNS Records": dns_count}
        metadata.propagate(self)
    except HTTPError as e:
        logger.error(f"Zone Sync HTTP Req Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info("Completed Cloudflare zones sync.")
    return metadata.model_dump()


@shared_task(bind=True)
def sync_cloudflare_zone(self: Task, db_id: int) -> dict[str, Any]:
    """
    TODO
    """
    metadata = CeleryMetaData(task="Sync Cloudflare Zone", result={"db_id": db_id})
    metadata.propagate(self)
    logger.info(f"Starting Cloudflare Zone Sync... (DB_ID: {db_id})")

    try:
        metadata.state = "Getting Zone..."
        metadata.current = 20
        metadata.propagate(self)
        zone = CloudflareZone.objects.get(id=db_id)

        metadata.state = "Pulling Zone..."
        metadata.current = 80
        metadata.propagate(self)
        zone.pull()

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.propagate(self)
    except CloudflareZone.DoesNotExist as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "Record Does Not Exist"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Zone Sync Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info(f"Completed Cloudflare zone sync. (DB_ID: {db_id})")
    return metadata.model_dump()

@shared_task(bind=True)
def sync_cloudflare_zone_dns_records(self: Task, db_id: int) -> dict[str, Any]:
    """
    TODO
    """
    metadata = CeleryMetaData(task="Sync Cloudflare Zone DNS", result={"db_id": db_id})
    metadata.propagate(self)
    logger.info(f"Starting Cloudflare Zone DNS Sync... (DB_ID: {db_id})")

    try:
        metadata.state = "Getting Zone..."
        metadata.current = 20
        metadata.propagate(self)
        zone = CloudflareZone.objects.get(id=db_id)

        metadata.state = "Pulling Zone..."
        metadata.current = 80
        metadata.propagate(self)
        zone.pull_dns_records()

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.propagate(self)
    except CloudflareZone.DoesNotExist as e:
        raise e
    except HTTPError as e:
        raise e
    except Exception as e:
        raise e

    logger.info(f"Completed Cloudflare Zone DNS Sync. (DB_ID: {db_id})")
    return metadata.model_dump()
