"""Shared helper functions and constants for D-Tools Cloud API endpoints."""

from dtools_mcp.config import config

BASE_API_URL = "https://dtcloudapi.d-tools.cloud/api/v1"


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
