"""Base models for the PokeAPI."""
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class NamedAPIResource(BaseModel):
    """A named resource in the PokeAPI."""

    name: str
    url: str

class PaginatedResponse(BaseModel, Generic[T]):
    """A paginated response from the PokeAPI."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]