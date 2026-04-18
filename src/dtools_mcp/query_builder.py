"""
Dynamic query parameter builder for D-Tools Cloud API.

This module provides utilities to build query parameters
based on common patterns (filtering, pagination, sorting, date ranges).
"""

import logging
from typing import Any
from datetime import datetime

logger = logging.getLogger(__name__)


class QueryBuilder:
    """Build query parameters for API endpoints using a fluent interface."""

    def __init__(self, endpoint_path: str = ""):
        """Initialize builder for an endpoint.

        Args:
            endpoint_path: Full API endpoint path (e.g., "/api/v1/Clients/GetClients")
                          Optional - only used for logging context.
        """
        self.endpoint_path = endpoint_path
        self.params = {}

    def add(self, name: str, value: Any) -> "QueryBuilder":
        """Add a query parameter.

        Args:
            name: Parameter name
            value: Parameter value (will be converted to appropriate type)

        Returns:
            Self for method chaining
        """
        if value is None:
            return self

        self.params[name] = self._convert_value(name, value)
        return self

    def add_if(self, name: str, value: Any, condition: bool) -> "QueryBuilder":
        """Add a parameter only if condition is true.

        Args:
            name: Parameter name
            value: Parameter value
            condition: Boolean condition

        Returns:
            Self for method chaining
        """
        if condition:
            self.add(name, value)
        return self

    def add_pagination(self, page: int = 1, page_size: int = 20) -> "QueryBuilder":
        """Add pagination parameters.

        Args:
            page: Page number (1-indexed)
            page_size: Items per page

        Returns:
            Self for method chaining
        """
        self.add("page", max(1, page))
        self.add("pageSize", max(1, min(page_size, 100)))  # Cap at 100
        return self

    def add_search(self, search_term: str | None) -> "QueryBuilder":
        """Add search parameter if provided.

        Args:
            search_term: Search string

        Returns:
            Self for method chaining
        """
        return self.add_if("search", search_term, bool(search_term))

    def add_date_range(
        self,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        field: str = "Created",
    ) -> "QueryBuilder":
        """Add date range filters.

        Args:
            from_date: Start date
            to_date: End date
            field: Date field (Created, Modified, etc.)

        Returns:
            Self for method chaining
        """
        if from_date:
            self.add(f"from{field}Date", from_date.isoformat())
        if to_date:
            self.add(f"to{field}Date", to_date.isoformat())
        return self

    def add_sort(self, sort_field: str | None) -> "QueryBuilder":
        """Add sort parameter.

        Args:
            sort_field: Field to sort by

        Returns:
            Self for method chaining
        """
        return self.add_if("sort", sort_field, bool(sort_field))

    def add_filters(self, **filters: Any) -> "QueryBuilder":
        """Add multiple filter parameters.

        Args:
            **filters: Named parameters to add

        Returns:
            Self for method chaining
        """
        for key, value in filters.items():
            self.add(key, value)
        return self

    def build(self) -> dict[str, Any]:
        """Get the built query parameters.

        Returns:
            Dictionary of query parameters
        """
        return self.params.copy()

    @staticmethod
    def _convert_value(name: str, value: Any) -> Any:
        """Convert value to appropriate type for API.

        Args:
            name: Parameter name (for context)
            value: Value to convert

        Returns:
            Converted value
        """
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            # Arrays are sent as repeated query params or comma-separated
            return value
        elif isinstance(value, datetime):
            return value.isoformat()
        return value


def build_query_params(endpoint_path: str, **kwargs: Any) -> dict[str, Any]:
    """Convenience function to build query params in one call.

    Args:
        endpoint_path: Full API endpoint path (optional, only for logging context)
        **kwargs: Parameters to add

    Returns:
        Dictionary of query parameters

    Example:
        >>> params = build_query_params(
        ...     "/api/v1/Clients/GetClients",
        ...     search="John",
        ...     page=1,
        ...     pageSize=20
        ... )
    """
    builder = QueryBuilder(endpoint_path)
    return builder.add_filters(**kwargs).build()
