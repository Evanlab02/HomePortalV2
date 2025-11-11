"""Contains models for the QBittorrent app."""

import json

from django.db.models import CharField, IntegerField
from requests import Session

from utils.models import BaseModel


class QBitServer(BaseModel):
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

    class Meta:
        """Meta configuration."""

        verbose_name = "QBittorrent Server"
        verbose_name_plural = "QBittorrent Servers"

    def login(self) -> Session:
        """
        Login into the QBittorrent instance.

        Authenticates with the QBittorrent server using the stored credentials and establishes
        a session for subsequent API calls.

        Returns:
            Session: The requests session for persisting the login if you
                want to do multiple actions.

        Raises:
            HTTPError: If the authentication request fails.
        """
        session = Session()
        response = session.post(
            f"{self.host}/api/v2/auth/login",
            data={"username": self.username, "password": self.password},
        )
        response.raise_for_status()
        return session

    def pull(self, session: Session | None = None) -> Session:
        """
        Pull the configuration from the QBittorrent server.

        Retrieves the current preferences from the QBittorrent server, updates the listen_port
        attribute, and saves the model instance.

        Args:
            session (Session | None): Optional existing session to reuse.
                If None, a new session is created.

        Returns:
            Session: The requests session for persisting the login if you
                want to do multiple actions.

        Raises:
            HTTPError: If the preferences request fails.
        """
        if not session:
            session = self.login()

        response = session.get(f"{self.host}/api/v2/app/preferences")
        response.raise_for_status()

        self.listen_port = int(response.json()["listen_port"])
        self.save()
        return session

    def push(self, session: Session | None = None) -> Session:
        """
        Push the configuration to the QBittorrent server.

        Sends the current listen_port setting to the QBittorrent server to update its preferences.

        Args:
            session (Session | None): Optional existing session to reuse.
                If None, a new session is created.

        Returns:
            Session: The requests session for persisting the login if you
                want to do multiple actions.

        Raises:
            HTTPError: If the set preferences request fails.
        """
        if not session:
            session = self.login()

        response = session.post(
            f"{self.host}/api/v2/app/setPreferences",
            data={"json": json.dumps({"listen_port": self.listen_port})},
        )
        response.raise_for_status()
        return session
