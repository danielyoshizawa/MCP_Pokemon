"""Exceptions for the PokeAPI client."""

from typing import Any, Dict, Optional


class PokeAPIError(Exception):
    """Base exception for PokeAPI errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: The error message.
            status_code: The HTTP status code.
            response: The response data.
        """
        super().__init__(message)
        self.status_code = status_code
        self.response = response or {}


class PokeAPIConnectionError(PokeAPIError):
    """Raised when there is a connection error."""


class PokeAPIResponseError(PokeAPIError):
    """Raised when the response contains an error."""


class PokeAPINotFoundError(PokeAPIResponseError):
    """Raised when a resource is not found."""


class PokeAPIRateLimitError(PokeAPIResponseError):
    """Raised when the rate limit is exceeded.""" 