"""Base HTTP client for the PokeAPI."""

from typing import Any, Dict, Optional
import json

import httpx

from mcp_pokemon.pokeapi.client.exceptions import (
    PokeAPIConnectionError,
    PokeAPINotFoundError,
    PokeAPIRateLimitError,
    PokeAPIResponseError,
)


class HTTPClient:
    """Base HTTP client for making API requests."""

    def __init__(self, base_url: str) -> None:
        """Initialize the HTTP client.

        Args:
            base_url: The base URL for the API.
        """
        self.base_url = base_url.rstrip("/")
        self._client: Optional[httpx.Client] = None

    def __enter__(self) -> "HTTPClient":
        """Enter the context manager."""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context manager."""
        self.close()

    @property
    def client(self) -> httpx.Client:
        """Get the HTTP client.

        Returns:
            The HTTP client.

        Raises:
            PokeAPIConnectionError: If the client is not connected.
        """
        if self._client is None:
            raise PokeAPIConnectionError("Client is not connected")
        return self._client

    def connect(self) -> None:
        """Connect to the API."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=30.0,
                follow_redirects=True,
            )

    def close(self) -> None:
        """Close the connection to the API."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle the response from the API.

        Args:
            response: The response from the API.

        Returns:
            The JSON response data.

        Raises:
            PokeAPINotFoundError: If the resource is not found.
            PokeAPIRateLimitError: If the rate limit is exceeded.
            PokeAPIResponseError: If the response contains an error.
        """
        try:
            response.raise_for_status()
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = {"message": "Invalid JSON response"}
            response.close()
            return data
        except httpx.HTTPStatusError as e:
            try:
                data = e.response.json()
            except json.JSONDecodeError:
                data = {"message": str(e)}
            
            if e.response.status_code == 404:
                raise PokeAPINotFoundError(
                    "Resource not found",
                    status_code=404,
                    response=data,
                )
            elif e.response.status_code == 429:
                raise PokeAPIRateLimitError(
                    "Rate limit exceeded",
                    status_code=429,
                    response=data,
                )
            else:
                raise PokeAPIResponseError(
                    f"HTTP {e.response.status_code}",
                    status_code=e.response.status_code,
                    response=data,
                )

    def _get(self, path: str, **params) -> dict:
        """Make a GET request to the API.

        Args:
            path: The path to request.
            **params: Additional query parameters.

        Returns:
            The response data.

        Raises:
            PokeAPINotFoundError: If the resource is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        try:
            response = self.client.get(path, params=params)
            if response.status_code != 200:
                error_data = response.json() if response.content else {}
                if response.status_code == 404:
                    raise PokeAPINotFoundError(
                        message="Resource not found",
                        response=error_data,
                        status_code=404
                    )
                elif response.status_code == 429:
                    raise PokeAPIRateLimitError(
                        message="Rate limit exceeded",
                        response=error_data,
                        status_code=429
                    )
                else:
                    raise PokeAPIResponseError(
                        message=f"HTTP {response.status_code}",
                        response=error_data,
                        status_code=response.status_code
                    )
            return response.json()
        except httpx.RequestError as e:
            raise PokeAPIConnectionError(message="Connection error") from e
