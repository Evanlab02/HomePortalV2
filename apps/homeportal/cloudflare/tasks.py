"""Contains celery tasks for cloudflare app."""

from logging import getLogger

from celery import shared_task

from cloudflare.models import CloudflareZone

logger = getLogger(__name__)


@shared_task
def sync_cloudflare_zones() -> None:
    """Synchronize all Cloudflare zones and DNS records.

    Fetches all zones from the Cloudflare API and syncs them with the local database.
    This includes creating new zones, updating existing zones, deleting removed zones,
    and pulling DNS records for all zones.

    Returns:
        None: This function does not return a value.
    """
    logger.info("Starting Cloudflare zones sync...")
    CloudflareZone.pull_all()
    logger.info("Completed Cloudflare zones sync.")
