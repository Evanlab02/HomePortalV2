"""Contains models for the QBittorrent app."""

import json

from django.db.models import CharField, IntegerField, Model
from requests import Session
from simple_history.models import HistoricalRecords

from app.exceptions import HomePortalHTTPError


class QBitServer(Model):
    """
    Model for managing the state of QBittorrent App configurations.

    NOTE: At this stage this model does not securely store passwords and therefore
    this is even more reason to ensure your apps are behind authentik and on a private network.

    Attributes:
        host (CharField): The QBittorrent server URL (max 30 characters, unique).
        username (CharField): The username for authentication (max 30 characters).
        password (CharField): The password for authentication (max 100 characters).
        listen_port (IntegerField): The port QBittorrent listens on for incoming connections.
        history (HistoricalRecords): Tracks historical changes to this model instance.
    """

    host = CharField(max_length=30, unique=True)
    username = CharField(max_length=30)
    password = CharField(max_length=100)
    listen_port = IntegerField(null=True, default=None)
    history = HistoricalRecords()

    def login(self) -> Session:
        """
        Login into the instance.

        Returns:
            session (Session): The requests session for persisting the login if you want to do multiple actions.
        """
        session = Session()
        response = session.post(
            f"{self.host}/api/v2/auth/login",
            data={"username": self.username, "password": self.password},
        )
        if response.status_code != 200:
            raise HomePortalHTTPError(status=response.status_code)
        return session

    def pull(self, session: Session | None) -> Session:
        """
        Pull the config from the QBittorrent server.

        Returns:
            session (Session): The requests session for persisting the login if you want to do multiple actions.
        """
        if not session:
            session = self.login()

        response = session.get(f"{self.host}/api/v2/app/preferences")
        if response.status_code != 200:
            raise HomePortalHTTPError(status=response.status_code)

        self.listen_port = int(response.json()["listen_port"])
        self.save()

    def push(self, session: Session | None) -> Session:
        """
        Push the config to the QBittorrent server.

        Returns:
            session (Session): The requests session for persisting the login if you want to do multiple actions.
        """
        if not session:
            session = self.login()

        response = session.post(
            f"{self.host}/api/v2/app/setPreferences",
            data={"json": json.dumps({"listen_port": self.listen_port})},
        )
        if response.status_code != 200:
            self.pull(session=session)
            raise HomePortalHTTPError(status=response.status_code)
