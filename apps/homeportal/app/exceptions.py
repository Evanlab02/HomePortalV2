"""Contains custom exceptions for the application."""


class HomePortalHTTPError(Exception):
    """Generic HomePortal App HTTP Error."""

    def __init__(self, status: int, *args) -> None:  # type: ignore
        """Init the home portal http error."""
        self.status = status
        super().__init__(*args)

    def __str__(self) -> str:
        """Stringify the exception."""
        return str(self.status)
