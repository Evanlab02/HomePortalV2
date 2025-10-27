"""Contains celery tasks for qbit app."""

from logging import getLogger

from celery import shared_task

from qbit.models import QBitServer

logger = getLogger(__name__)

@shared_task
def sync_forwarded_port_to_qbit() -> None:
    """
    Celery task to synchronize the forwarded port from the config file to all QBittorrent servers.

    This task reads the forwarded port from './qbit/config/forwarded_port' and updates all
    QBitServer instances if the port differs from the current listen_port. It first pulls the
    current configuration from each server, compares ports, updates the database, and pushes
    the new configuration back to the server.

    Returns:
        None
    """
    port = 0
    with open("./qbit/config/forwarded_port", "r") as f:
        port: str | int = f.read().strip()
        port = int(port)

    records = QBitServer.objects.all()
    for record in records:
        session = record.pull()
        if port == record.listen_port:
            logger.info(f"Ports already match for {record.host}.")
            continue
        record.listen_port = port
        record.save()
        record.push(session=session)
