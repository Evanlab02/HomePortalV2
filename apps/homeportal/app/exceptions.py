"""Contains custom exceptions for the application."""


class HomePortalHTTPError(Exception):

    def __init__(self, status: int, *args):
        """Init the home portal http error."""
        self.status = status
        super().__init__(*args)

    def __str__(self):
        """Stringify the exception."""
        return self.status
