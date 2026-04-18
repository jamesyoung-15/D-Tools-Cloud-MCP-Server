"""D-Tools Cloud API - Quotes endpoints."""

import logging
from typing import Any

import httpx

from dtools_mcp.config import config
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_quotes(opportunity_id: str) -> dict[str, Any]:
    """Retrieve all quotes for a specific opportunity from D-Tools Cloud.

    Args:
        opportunity_id: The UUID of the opportunity to retrieve quotes for (required).

    Returns:
        API response containing list of quotes for the opportunity.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or opportunity_id is invalid.
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
            f"{BASE_API_URL}/Quotes/GetQuotes",
            params={"opportunityId": opportunity_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def get_quote_details(quote_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific quote.

    Args:
        quote_id: The UUID of the quote to retrieve.

    Returns:
        API response containing quote details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not quote_id:
        raise ValueError("quote_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Quotes/GetQuote",
            params={"id": quote_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()
