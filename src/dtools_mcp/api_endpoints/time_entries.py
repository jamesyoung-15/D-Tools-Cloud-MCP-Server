"""D-Tools Cloud API - Time Entries endpoints."""

import logging
from typing import Any
from datetime import datetime

import httpx

from dtools_mcp.config import config
from dtools_mcp.query_builder import QueryBuilder
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_time_entries(
    types: list[str] | None = None,
    resources: list[str] | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    client_ids: list[str] | None = None,
    project_ids: list[str] | None = None,
    service_call_ids: list[str] | None = None,
    labor_types: list[str] | None = None,
    overtimes_only: bool = False,
    include_archived: bool = False,
    include_total_count: bool = False,
    search: str | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """Retrieve a list of time entries from D-Tools Cloud.

    Args:
        types: Filter by time entry types (optional)
        resources: Filter by resources/employees (optional)
        from_date: Filter by entry date start (optional)
        to_date: Filter by entry date end (optional)
        client_ids: Filter by client IDs (optional)
        project_ids: Filter by project IDs (optional)
        service_call_ids: Filter by service call IDs (optional)
        labor_types: Filter by labor types (optional)
        overtimes_only: Return only overtime entries (default: False)
        include_archived: Include archived time entries (default: False)
        include_total_count: Include total count in response (default: False)
        search: Search time entries (optional)
        sort: Sort field (optional)
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        API response containing list of time entries.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    builder = QueryBuilder("/api/v1/TimeEntries/GetTimeEntries")
    builder.add_filters(
        types=types,
        resources=resources,
        clientIds=client_ids,
        projectIds=project_ids,
        serviceCallIds=service_call_ids,
        laborTypes=labor_types,
        overtimesOnly=overtimes_only,
        includeArchived=include_archived,
        includeTotalCount=include_total_count,
    )
    builder.add_date_range(from_date, to_date, "")
    builder.add_search(search)
    builder.add_sort(sort)
    builder.add_pagination(page, page_size)

    params = builder.build()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/TimeEntries/GetTimeEntries",
            params=params,
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()