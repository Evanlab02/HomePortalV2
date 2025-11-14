"""Contains celery tasks for qbit app."""

from logging import getLogger
from typing import Any

from celery import Task, shared_task
from requests import HTTPError

from app.schemas import CeleryMetaData
from qbit.models import QBitServer

logger = getLogger(__name__)


@shared_task(bind=True)
def sync_forwarded_port_to_qbit(self: Task) -> dict[str, Any]:
    """Synchronize the forwarded port from the config file to all QBittorrent servers.

    This task reads the forwarded port from './qbit/config/forwarded_port' and updates all
    QBitServer instances if the port differs from the current listen_port. It first pulls the
    current configuration from each server, compares ports, updates the database, and pushes
    the new configuration back to the server.

    Args:
        self (Task): The Celery task instance.

    Returns:
        dict[str, Any]: Task metadata including state, progress, and results.

    Raises:
        FileNotFoundError: If the config file does not exist.
        HTTPError: If the HTTP request to the server fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Sync Forwarded Port to Qbit")
    metadata.propagate(self)
    logger.info("Starting Forwarded Port Sync...")

    try:
        metadata.state = "Reading Port Config..."
        metadata.current = 20
        metadata.propagate(self)

        with open("./qbit/config/forwarded_port", "r") as f:
            port = int(f.read().strip())

        metadata.state = "Getting Servers..."
        metadata.current = 40
        metadata.propagate(self)
        servers = QBitServer.objects.all()

        metadata.state = "Syncing Servers..."
        metadata.current = 60
        metadata.propagate(self)

        updated_count = 0
        for server in servers:
            session = server.login()
            server.pull(session=session)
            if port != server.listen_port:
                server.listen_port = port
                server.save()
                server.push(session=session)
                updated_count += 1

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result = {"Updated Servers": updated_count, "Total Servers": servers.count()}
        metadata.propagate(self)
    except FileNotFoundError as e:
        logger.error(f"Port Sync Failed: {e}")
        metadata.state = "Config File Not Found"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"Port Sync Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Port Sync Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info("Completed Forwarded Port Sync.")
    return metadata.model_dump()


@shared_task(bind=True)
def pull_qbit_server(self: Task, db_id: int) -> dict[str, Any]:
    """Pull configuration from a single QBittorrent server.

    Retrieves the current configuration from a QBittorrent server and updates
    the corresponding database record.

    Args:
        self (Task): The Celery task instance.
        db_id (int): The database ID of the QBitServer record.

    Returns:
        dict[str, Any]: Task metadata including state, progress, and results.

    Raises:
        QBitServer.DoesNotExist: If the server record does not exist.
        HTTPError: If the HTTP request to the server fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Pull Qbit Server", result={"db_id": db_id})
    metadata.propagate(self)
    logger.info(f"Starting Qbit Server Pull... (DB_ID: {db_id})")

    try:
        metadata.state = "Getting Server..."
        metadata.current = 20
        metadata.propagate(self)
        server = QBitServer.objects.get(id=db_id)

        metadata.state = "Pulling Config..."
        metadata.current = 80
        metadata.propagate(self)
        session = server.login()
        server.pull(session=session)

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result["host"] = server.host
        metadata.result["listen_port"] = server.listen_port
        metadata.propagate(self)
    except QBitServer.DoesNotExist as e:
        logger.error(f"Server Pull Failed: {e}")
        metadata.state = "Record Does Not Exist"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"Server Pull Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Server Pull Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info(f"Completed Qbit Server Pull. (DB_ID: {db_id})")
    return metadata.model_dump()


@shared_task(bind=True)
def push_qbit_server(self: Task, db_id: int) -> dict[str, Any]:
    """Push configuration to a single QBittorrent server.

    Sends the configuration from the database record to the QBittorrent server.

    Args:
        self (Task): The Celery task instance.
        db_id (int): The database ID of the QBitServer record.

    Returns:
        dict[str, Any]: Task metadata including state, progress, and results.

    Raises:
        QBitServer.DoesNotExist: If the server record does not exist.
        HTTPError: If the HTTP request to the server fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Push Qbit Server", result={"db_id": db_id})
    metadata.propagate(self)
    logger.info(f"Starting Qbit Server Push... (DB_ID: {db_id})")

    try:
        metadata.state = "Getting Server..."
        metadata.current = 20
        metadata.propagate(self)
        server = QBitServer.objects.get(id=db_id)

        metadata.state = "Pushing Config..."
        metadata.current = 80
        metadata.propagate(self)
        session = server.login()
        server.push(session=session)

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result["host"] = server.host
        metadata.result["listen_port"] = server.listen_port
        metadata.propagate(self)
    except QBitServer.DoesNotExist as e:
        logger.error(f"Server Push Failed: {e}")
        metadata.state = "Record Does Not Exist"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except HTTPError as e:
        logger.error(f"Server Push Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"Server Push Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info(f"Completed Qbit Server Push. (DB_ID: {db_id})")
    return metadata.model_dump()


@shared_task(bind=True)
def pull_all_qbit_servers(self: Task) -> dict[str, Any]:
    """Pull configuration from all QBittorrent servers.

    Retrieves the current configuration from all QBittorrent servers and updates
    their corresponding database records.

    Args:
        self (Task): The Celery task instance.

    Returns:
        dict[str, Any]: Task metadata including state, progress, and results.

    Raises:
        HTTPError: If an HTTP request to a server fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Pull All Qbit Servers")
    metadata.propagate(self)
    logger.info("Starting All Qbit Server Pulls...")

    try:
        metadata.state = "Getting Servers..."
        metadata.current = 20
        metadata.propagate(self)
        servers = QBitServer.objects.all()

        metadata.state = "Pulling Servers..."
        metadata.current = 40
        metadata.propagate(self)

        success_count = 0
        error_count = 0
        for server in servers:
            try:
                session = server.login()
                server.pull(session=session)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to pull server {server.host}: {e}")
                error_count += 1

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result = {
            "Total Servers": servers.count(),
            "Successful Pulls": success_count,
            "Failed Pulls": error_count,
        }
        metadata.propagate(self)
    except HTTPError as e:
        logger.error(f"All Server Pulls Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"All Server Pulls Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info("Completed All Qbit Server Pulls.")
    return metadata.model_dump()


@shared_task(bind=True)
def push_all_qbit_servers(self: Task) -> dict[str, Any]:
    """Push configuration to all QBittorrent servers.

    Sends the configuration from all database records to their corresponding
    QBittorrent servers.

    Args:
        self (Task): The Celery task instance.

    Returns:
        dict[str, Any]: Task metadata including state, progress, and results.

    Raises:
        HTTPError: If an HTTP request to a server fails.
        Exception: For any other unexpected errors.
    """
    metadata = CeleryMetaData(task="Push All Qbit Servers")
    metadata.propagate(self)
    logger.info("Starting All Qbit Server Pushes...")

    try:
        metadata.state = "Getting Servers..."
        metadata.current = 20
        metadata.propagate(self)
        servers = QBitServer.objects.all()

        metadata.state = "Pushing Servers..."
        metadata.current = 40
        metadata.propagate(self)

        success_count = 0
        error_count = 0
        for server in servers:
            try:
                session = server.login()
                server.push(session=session)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to push server {server.host}: {e}")
                error_count += 1

        metadata.state = "COMPLETED"
        metadata.current = 100
        metadata.result = {
            "Total Servers": servers.count(),
            "Successful Pushes": success_count,
            "Failed Pushes": error_count,
        }
        metadata.propagate(self)
    except HTTPError as e:
        logger.error(f"All Server Pushes Failed: {e}")
        metadata.state = "HTTP Request Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e
    except Exception as e:
        logger.error(f"All Server Pushes Failed: {e}")
        metadata.state = "Unexpected Failure"
        metadata.current = 100
        metadata.propagate(self)
        raise e

    logger.info("Completed All Qbit Server Pushes.")
    return metadata.model_dump()
