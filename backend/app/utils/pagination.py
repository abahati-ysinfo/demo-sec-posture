from math import ceil
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters"""

    skip: int = 0
    limit: int = 100

    @property
    def page(self) -> int:
        """Calculate current page number (1-indexed)"""
        return (self.skip // self.limit) + 1

    @property
    def offset(self) -> int:
        """Alias for skip for clarity"""
        return self.skip


class PaginationMeta(BaseModel):
    """Pagination metadata"""

    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse[T](BaseModel):
    """Generic paginated response"""

    items: list[T]
    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool


def paginate[T](
    items: list[T], total: int, skip: int, limit: int
) -> PaginatedResponse[T]:
    """Create paginated response with metadata"""
    page = (skip // limit) + 1 if limit > 0 else 1
    pages = ceil(total / limit) if limit > 0 else 0
    has_next = skip + limit < total
    has_prev = skip > 0

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        pages=pages,
        has_next=has_next,
        has_prev=has_prev,
    )
