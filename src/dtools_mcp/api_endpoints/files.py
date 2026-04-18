"""D-Tools Cloud API - Files endpoints."""

import logging
from typing import Any

import httpx

from dtools_mcp.config import config
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def get_file_details(file_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific file.

    Args:
        file_id: The UUID of the file to retrieve.

    Returns:
        API response containing file details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not file_id:
        raise ValueError("file_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Files/GetFile",
            params={"id": file_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()