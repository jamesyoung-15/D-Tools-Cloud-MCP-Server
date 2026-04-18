"""D-Tools Cloud API - Purchase Orders endpoints."""

import logging
from typing import Any
from datetime import datetime

import httpx

from dtools_mcp.config import config
from dtools_mcp.query_builder import QueryBuilder
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_purchase_orders(
    suppliers: list[str] | None = None,
    project_ids: list[str] | None = None,
    statuses: list[str] | None = None,
    from_ordered_date: datetime | None = None,
    to_ordered_date: datetime | None = None,
    from_received_date: datetime | None = None,
    to_received_date: datetime | None = None,
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
    """Retrieve a list of purchase orders from D-Tools Cloud.

    Args:
        suppliers: Filter by suppliers (optional)
        project_ids: Filter by project IDs (optional)
        statuses: Filter by purchase order statuses (optional)
        from_ordered_date: Filter by order date start (optional)
        to_ordered_date: Filter by order date end (optional)
        from_received_date: Filter by received date start (optional)
        to_received_date: Filter by received date end (optional)
        from_created_date: Filter by creation date start (optional)
        to_created_date: Filter by creation date end (optional)
        from_modified_date: Filter by modification date start (optional)
        to_modified_date: Filter by modification date end (optional)
        include_archived: Include archived purchase orders (default: False)
        include_total_count: Include total count in response (default: False)
        search: Search purchase orders by supplier or number (optional)
        sort: Sort field (optional)
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        API response containing list of purchase orders.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    builder = QueryBuilder("/api/v1/PurchaseOrders/GetPurchaseOrders")
    builder.add_filters(
        suppliers=suppliers,
        projectIds=project_ids,
        statuses=statuses,
        includeArchived=include_archived,
        includeTotalCount=include_total_count,
    )
    builder.add_date_range(from_ordered_date, to_ordered_date, "Ordered")
    builder.add_date_range(from_received_date, to_received_date, "Received")
    builder.add_date_range(from_created_date, to_created_date, "Created")
    builder.add_date_range(from_modified_date, to_modified_date, "Modified")
    builder.add_search(search)
    builder.add_sort(sort)
    builder.add_pagination(page, page_size)

    params = builder.build()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/PurchaseOrders/GetPurchaseOrders",
            params=params,
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def get_purchase_order_details(purchase_order_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific purchase order.

    Args:
        purchase_order_id: The UUID of the purchase order to retrieve.

    Returns:
        API response containing purchase order details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not purchase_order_id:
        raise ValueError("purchase_order_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/PurchaseOrders/GetPurchaseOrder",
            params={"id": purchase_order_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()