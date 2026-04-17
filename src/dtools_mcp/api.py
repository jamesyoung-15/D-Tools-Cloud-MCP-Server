"""D-Tools Cloud API wrapper for MCP server.

This module provides async functions to interact with D-Tools Cloud API endpoints.
Credentials are loaded from environment variables at module initialization.

References:
    - API Docs: https://docs.d-tools.cloud/en/collections/7640732-cloud-api-documentation
    - Swagger: https://dtcloudapi.d-tools.cloud/swagger/v1/swagger.json
"""

import logging
from typing import Any

import httpx

from dtools_mcp.config import config

logger = logging.getLogger(__name__)

# D-Tools Cloud API base URL
BASE_URL = "https://dtcloudapi.d-tools.cloud/api/v1"


def get_headers() -> dict[str, str]:
    """Get authentication headers for D-Tools Cloud API requests.

    Returns:
        Headers with Authorization and API key.
    """
    headers = {
        "Content-Type": "application/json",
    }

    if config.dtools_api_key:
        headers["X-API-Key"] = config.dtools_api_key

    if config.dtools_auth_token:
        headers["Authorization"] = f"Basic {config.dtools_auth_token}"

    return headers


async def list_clients() -> dict[str, Any]:
    """Retrieve a list of all clients in D-Tools Cloud.

    Returns:
        API response containing list of clients.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If credentials are not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools Cloud credentials not configured. "
            "Please set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    headers = get_headers()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/Clients/GetClients",
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"API error listing clients: {e.response.status_code} - {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error listing clients: {e}")
            raise


async def get_client_details(client_id: str) -> dict[str, Any]:
    """Retrieve details for a specific client.

    Args:
        client_id: The ID of the client to retrieve.

    Returns:
        API response containing client details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If credentials are not configured or client_id is invalid.
    """
    if not client_id or not isinstance(client_id, str):
        raise ValueError("client_id must be a non-empty string")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools Cloud credentials not configured. "
            "Please set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    headers = get_headers()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/Clients/GetClient",
                headers=headers,
                params={"id": client_id},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"API error getting client {client_id}: {e.response.status_code} - {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error getting client {client_id}: {e}")
            raise


async def list_projects(client_id: str | None = None) -> dict[str, Any]:
    """Retrieve a list of projects in D-Tools Cloud.

    Optionally filter by client ID.

    Args:
        client_id: Optional client ID to filter projects by.

    Returns:
        API response containing list of projects.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If credentials are not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools Cloud credentials not configured. "
            "Please set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    headers = get_headers()

    # Build query parameters
    params = {}
    if client_id:
        params["clientIds"] = [client_id]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/Projects/GetProjects",
                headers=headers,
                params=params,
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"API error listing projects: {e.response.status_code} - {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error listing projects: {e}")
            raise


async def get_project_details(project_id: str) -> dict[str, Any]:
    """Retrieve details for a specific project.

    Args:
        project_id: The ID of the project to retrieve.

    Returns:
        API response containing project details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If credentials are not configured or project_id is invalid.
    """
    if not project_id or not isinstance(project_id, str):
        raise ValueError("project_id must be a non-empty string")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools Cloud credentials not configured. "
            "Please set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    headers = get_headers()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/Projects/GetProject",
                headers=headers,
                params={"id": project_id},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"API error getting project {project_id}: {e.response.status_code} - {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error getting project {project_id}: {e}")
            raise
