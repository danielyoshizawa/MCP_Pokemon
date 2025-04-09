"""Base HTTP client for making requests to external APIs."""

import aiohttp
from typing import Any, Dict, Optional

from mcp_pokemon.pokeapi.client.exceptions import (
    PokeAPIConnectionError,
    PokeAPINotFoundError,
    PokeAPIRateLimitError,
    PokeAPIResponseError,
)

class HTTPClient:
    """Base HTTP client for making requests to external APIs."""

    def __init__(self, base_url: str) -> None:
        """Initialize the HTTP client.
        
        Args:
            base_url: The base URL for the API.
        """
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None

    async def connect(self) -> None:
        """Create and initialize the HTTP session."""
        if not self._session:
            self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def __aenter__(self) -> 'HTTPClient':
        """Enter the async context manager."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the async context manager."""
        await self.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle the HTTP response and return the JSON data.
        
        Args:
            response: The HTTP response from the request.
            
        Returns:
            The JSON data from the response.
            
        Raises:
            PokeAPINotFoundError: If the resource was not found.
            PokeAPIRateLimitError: If the rate limit was exceeded.
            PokeAPIResponseError: If there was an error with the response.
        """
        if response.status == 404:
            raise PokeAPINotFoundError("Resource not found")
        elif response.status == 429:
            raise PokeAPIRateLimitError("Rate limit exceeded")
        elif response.status >= 400:
            raise PokeAPIResponseError(f"HTTP {response.status}: {await response.text()}")
        
        return await response.json()

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API.
        
        Args:
            path: The path to request.
            params: Optional query parameters.
            
        Returns:
            The JSON response data.
            
        Raises:
            PokeAPIConnectionError: If there was an error connecting to the API.
            PokeAPINotFoundError: If the resource was not found.
            PokeAPIRateLimitError: If the rate limit was exceeded.
            PokeAPIResponseError: If there was an error with the response.
        """
        if not self._session:
            raise PokeAPIConnectionError("Client is not connected")

        try:
            url = f"{self.base_url}/{path}"
            async with self._session.get(url, params=params) as response:
                return await self._handle_response(response)
        except aiohttp.ClientError as ex:
            raise PokeAPIConnectionError(f"Failed to connect to API: {ex}")
