"""D-Tools Cloud API - Opportunities endpoints."""

import logging
from typing import Any
from datetime import datetime

import httpx

from dtools_mcp.config import config
from dtools_mcp.query_builder import QueryBuilder
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_opportunities(
    types: list[str] | None = None,
    client_ids: list[str] | None = None,
    stage_groups: list[str] | None = None,
    stages: list[str] | None = None,
    priorities: list[str] | None = None,
    owners: list[str] | None = None,
    from_estimated_close_date: datetime | None = None,
    to_estimated_close_date: datetime | None = None,
    from_actual_close_date: datetime | None = None,
    to_actual_close_date: datetime | None = None,
    from_created_date: datetime | None = None,
    to_created_date: datetime | None = None,
    from_modified_date: datetime | None = None,
    to_modified_date: datetime | None = None,
    include_archived: bool = False,
    include_total_count: bool = False,
    search: str | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """Retrieve a list of opportunities from D-Tools Cloud.

    Args:
        types: Filter by opportunity types (optional)
        client_ids: Filter by client IDs (optional)
        stage_groups: Filter by stage groups (optional)
        stages: Filter by stages (optional)
        priorities: Filter by priorities (optional)
        owners: Filter by owner names (optional)
        from_estimated_close_date: Filter by estimated close date start (optional)
        to_estimated_close_date: Filter by estimated close date end (optional)
        from_actual_close_date: Filter by actual close date start (optional)
        to_actual_close_date: Filter by actual close date end (optional)
        from_created_date: Filter by creation date start (optional)
        to_created_date: Filter by creation date end (optional)
        from_modified_date: Filter by modification date start (optional)
        to_modified_date: Filter by modification date end (optional)
        include_archived: Include archived opportunities (default: False)
        include_total_count: Include total count in response (default: False)
        search: Search opportunities by name (optional)
        sort: Sort field (optional)
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        API response containing list of opportunities.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    builder = QueryBuilder("/api/v1/Opportunities/GetOpportunities")
    builder.add_filters(
        types=types,
        clientIds=client_ids,
        stageGroups=stage_groups,
        stages=stages,
        priorities=priorities,
        owners=owners,
        includeArchived=include_archived,
        includeTotalCount=include_total_count,
    )
    builder.add_date_range(
        from_estimated_close_date, to_estimated_close_date, "EstimatedClose"
    )
    builder.add_date_range(from_actual_close_date, to_actual_close_date, "ActualClose")
    builder.add_date_range(from_created_date, to_created_date, "Created")
    builder.add_date_range(from_modified_date, to_modified_date, "Modified")
    builder.add_search(search)
    builder.add_sort(sort)
    builder.add_pagination(page, page_size)

    params = builder.build()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Opportunities/GetOpportunities",
            params=params,
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def get_opportunity_details(opportunity_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific opportunity.

    Args:
        opportunity_id: The UUID of the opportunity to retrieve.

    Returns:
        API response containing opportunity details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not opportunity_id:
        raise ValueError("opportunity_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Opportunities/GetOpportunity",
            params={"id": opportunity_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()
