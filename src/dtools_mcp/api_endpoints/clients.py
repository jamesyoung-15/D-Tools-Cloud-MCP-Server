"""D-Tools Cloud API - Clients endpoints."""

import logging
from typing import Any
from datetime import datetime

import httpx

from dtools_mcp.config import config
from dtools_mcp.query_builder import QueryBuilder
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_clients(
    types: list[str] | None = None,
    owners: list[str] | None = None,
    from_created_date: datetime | None = None,
    to_created_date: datetime | None = None,
    from_modified_date: datetime | None = None,
    to_modified_date: datetime | None = None,
    include_inactive: bool = False,
    include_total_count: bool = False,
    search: str | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """Retrieve a list of clients from D-Tools Cloud.

    Args:
        types: Filter by client types (optional)
        owners: Filter by owner names (optional)
        from_created_date: Filter by creation date start (optional)
        to_created_date: Filter by creation date end (optional)
        from_modified_date: Filter by modification date start (optional)
        to_modified_date: Filter by modification date end (optional)
        include_inactive: Include inactive clients (default: False)
        include_total_count: Include total count in response (default: False)
        search: Search clients by name/email (optional)
        sort: Sort field (optional)
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        API response containing list of clients.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    builder = QueryBuilder("/api/v1/Clients/GetClients")
    builder.add_filters(
        types=types,
        owners=owners,
        includeInactive=include_inactive,
        includeTotalCount=include_total_count,
    )
    builder.add_date_range(from_created_date, to_created_date, "Created")
    builder.add_date_range(from_modified_date, to_modified_date, "Modified")
    builder.add_search(search)
    builder.add_sort(sort)
    builder.add_pagination(page, page_size)

    params = builder.build()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Clients/GetClients",
            params=params,
            headers=get_headers(),
        )
        if response.status_code >= 400:
            logger.error(
                f"Failed to list clients: "
                f"Status {response.status_code} - {response.text}"
            )
        response.raise_for_status()
        return response.json()


async def get_client_details(client_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific client.

    Args:
        client_id: The UUID of the client to retrieve.

    Returns:
        API response containing client details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not client_id:
        raise ValueError("client_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Clients/GetClient",
            params={"id": client_id},
            headers=get_headers(),
        )
        if response.status_code >= 400:
            logger.error(
                f"Failed to get client {client_id}: "
                f"Status {response.status_code} - {response.text}"
            )
        response.raise_for_status()
        return response.json()


async def create_client(client_data: dict[str, Any]) -> str:
    """Create a new client in D-Tools Cloud.

    Args:
        client_data: Dictionary containing client fields.
            Required: name
            Optional: type, email, phone, fax, website, owner, isActive,
                     billingAddress, siteAddresses, contacts, etc.

            Address object structure (billingAddress, siteAddresses):
            {
                "name": str (optional),
                "addressLine1": str,
                "addressLine2": str (optional),
                "city": str,
                "state": str,
                "postalCode": str,
                "country": str
            }

            Contact object structure (contacts array):
            {
                "id": str (optional UUID),
                "name": str,
                "firstName": str,
                "lastName": str,
                "company": str (optional),
                "title": str (optional),
                "email": str,
                "secondaryEmail": str (optional),
                "mobile": str (optional),
                "phone": str (optional),
                "fax": str (optional),
                "addressLine1": str (optional),
                "addressLine2": str (optional),
                "city": str (optional),
                "state": str (optional),
                "postalCode": str (optional),
                "country": str (optional),
                "notes": str (optional),
                "isActive": bool (optional),
                "isPrimary": bool (optional)
            }

    Returns:
        The UUID of the newly created client.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or required fields are missing.
    """
    if not client_data:
        raise ValueError("client_data must not be empty")

    # Validate required fields
    if not client_data.get("name"):
        raise ValueError("client_data must contain 'name' field (required)")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_API_URL}/Clients/CreateClient",
            json=client_data,
            headers=get_headers(),
        )
        if response.status_code >= 400:
            error_details = response.text
            try:
                error_json = response.json()
                error_details = error_json
            except Exception:
                pass
            logger.error(f"API Error: {response.status_code} - {error_details}")
            response.raise_for_status()
        return response.json()


async def update_client(client_id: str, client_data: dict[str, Any]) -> str:
    """Update an existing client in D-Tools Cloud.

    Args:
        client_id: The UUID of the client to update.
        client_data: Dictionary containing client fields to update.
            Updateable fields: name, type, email, phone, fax, website, owner,
                             isExemptFromTax, isActive, billingAddress,
                             siteAddresses, contacts, etc.

            Address object structure (billingAddress, siteAddresses):
            {
                "name": str (optional),
                "addressLine1": str,
                "addressLine2": str (optional),
                "city": str,
                "state": str,
                "postalCode": str,
                "country": str
            }

            Contact object structure (contacts array):
            {
                "id": str (optional UUID),
                "name": str,
                "firstName": str,
                "lastName": str,
                "company": str (optional),
                "title": str (optional),
                "email": str,
                "secondaryEmail": str (optional),
                "mobile": str (optional),
                "phone": str (optional),
                "fax": str (optional),
                "addressLine1": str (optional),
                "addressLine2": str (optional),
                "city": str (optional),
                "state": str (optional),
                "postalCode": str (optional),
                "country": str (optional),
                "notes": str (optional),
                "isActive": bool (optional),
                "isPrimary": bool (optional)
            }

    Returns:
        The UUID of the updated client.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not client_id:
        raise ValueError("client_id is required")

    if not client_data:
        raise ValueError("client_data must contain at least one field to update")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_API_URL}/Clients/UpdateClient",
            params={"id": client_id},
            json=client_data,
            headers=get_headers(),
        )
        if response.status_code >= 400:
            error_details = response.text
            try:
                error_json = response.json()
                error_details = error_json
            except Exception:
                pass
            logger.error(f"API Error: {response.status_code} - {error_details}")
            response.raise_for_status()
        return response.json()
