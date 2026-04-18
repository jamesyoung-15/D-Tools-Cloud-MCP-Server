"""D-Tools Cloud API - ChangeOrders endpoints."""

import logging
from typing import Any

import httpx

from dtools_mcp.config import config
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_change_orders(
    project_id: str,
) -> dict[str, Any]:
    """Retrieve a list of change orders for a specific project.

    Args:
        project_id: The UUID of the project to retrieve change orders for (required).

    Returns:
        API response containing list of change orders.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or required parameters are missing.
    """
    if not project_id:
        raise ValueError("project_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/ChangeOrders/GetChangeOrders",
            params={"projectId": project_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def get_change_order_details(change_order_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific change order.

    Args:
        change_order_id: The UUID of the change order to retrieve.

    Returns:
        API response containing change order details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not change_order_id:
        raise ValueError("change_order_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/ChangeOrders/GetChangeOrder",
            params={"id": change_order_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()
