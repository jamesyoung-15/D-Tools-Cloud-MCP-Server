"""D-Tools Cloud MCP Tools - Clients resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    get_client_details,
    create_client,
    update_client,
    list_clients,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_all_clients(
    types: list[str] | None = None,
    owners: list[str] | None = None,
    search: str | None = None,
    include_inactive: bool = False,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all clients from D-Tools Cloud with optional filtering.

    Supports filtering by type, owner, search terms, and date ranges.

    Args:
        types: Filter by client types (e.g., ["Business", "Individual"])
        owners: Filter by owner names
        search: Search by client name or details
        include_inactive: Include inactive clients (default: False)
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and client list, or error details.
    """
    try:
        result = await list_clients(
            types=types,
            owners=owners,
            search=search,
            include_inactive=include_inactive,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get clients: {e}")
        return {"success": False, "error": f"Failed to retrieve clients: {str(e)}"}


@mcp.tool()
async def get_client_info(client_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific client.

    Provides comprehensive details about a client including their contact information,
    address, client type, and modification history.

    Args:
        client_id: The unique ID of the client (required).

    Returns:
        Dictionary with success status and client details, or error information.
    """
    try:
        result = await get_client_details(client_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get client {client_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve client: {str(e)}"}


@mcp.tool()
async def create_new_client(
    name: str,
    client_type: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    fax: str | None = None,
    website: str | None = None,
    owner: str | None = None,
    is_active: bool | None = None,
    is_exempt_from_tax: bool | None = None,
    billing_address: dict[str, Any] | None = None,
    site_addresses: list[dict[str, Any]] | None = None,
    contacts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create a new client in D-Tools Cloud.

    Creates a new client with the specified details and returns the client UUID.

    Args:
        name: The client name (required).
        client_type: Type of client (e.g., "Business", "Individual").
        email: Primary email address.
        phone: Phone number.
        fax: Fax number.
        website: Website URL.
        owner: Owner name or ID.
        is_active: Whether the client is active (default: True).
        is_exempt_from_tax: Whether the client is exempt from tax.
        billing_address: Billing address object with keys: addressLine1, addressLine2, city, state, postalCode, country.
        site_addresses: List of site address objects (same structure as billing_address).
        contacts: List of contact objects with keys: name, firstName, lastName, email, phone, etc.

    Returns:
        Dictionary with success status and the new client UUID, or error details.
    """
    try:
        client_data: dict[str, Any] = {"name": name}

        # Add optional fields if provided
        if client_type is not None:
            client_data["type"] = client_type
        if email is not None:
            client_data["email"] = email
        if phone is not None:
            client_data["phone"] = phone
        if fax is not None:
            client_data["fax"] = fax
        if website is not None:
            client_data["website"] = website
        if owner is not None:
            client_data["owner"] = owner
        if is_active is not None:
            client_data["isActive"] = is_active
        if is_exempt_from_tax is not None:
            client_data["isExemptFromTax"] = is_exempt_from_tax
        if billing_address is not None:
            client_data["billingAddress"] = billing_address
        if site_addresses is not None:
            client_data["siteAddresses"] = site_addresses
        if contacts is not None:
            client_data["contacts"] = contacts

        result = await create_client(client_data)
        return {
            "success": True,
            "data": result,
            "message": f"Client created successfully. ID: {result}",
        }
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to create client: {e}")
        return {"success": False, "error": f"Failed to create client: {str(e)}"}


@mcp.tool()
async def update_existing_client(
    client_id: str,
    name: str | None = None,
    client_type: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    fax: str | None = None,
    website: str | None = None,
    owner: str | None = None,
    is_active: bool | None = None,
    is_exempt_from_tax: bool | None = None,
    billing_address: dict[str, Any] | None = None,
    site_addresses: list[dict[str, Any]] | None = None,
    contacts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Update an existing client in D-Tools Cloud.

    Updates the specified fields of an existing client.

    Args:
        client_id: The unique ID of the client to update (required).
        name: The client name.
        client_type: Type of client (e.g., "Business", "Individual").
        email: Primary email address.
        phone: Phone number.
        fax: Fax number.
        website: Website URL.
        owner: Owner name or ID.
        is_active: Whether the client is active.
        is_exempt_from_tax: Whether the client is exempt from tax.
        billing_address: Billing address object with keys: addressLine1, addressLine2, city, state, postalCode, country.
        site_addresses: List of site address objects (same structure as billing_address).
        contacts: List of contact objects with keys: name, firstName, lastName, email, phone, etc.

    Returns:
        Dictionary with success status and the updated client UUID, or error details.
    """
    try:
        client_data: dict[str, Any] = {}

        # Add fields to update if provided
        if name is not None:
            client_data["name"] = name
        if client_type is not None:
            client_data["type"] = client_type
        if email is not None:
            client_data["email"] = email
        if phone is not None:
            client_data["phone"] = phone
        if fax is not None:
            client_data["fax"] = fax
        if website is not None:
            client_data["website"] = website
        if owner is not None:
            client_data["owner"] = owner
        if is_active is not None:
            client_data["isActive"] = is_active
        if is_exempt_from_tax is not None:
            client_data["isExemptFromTax"] = is_exempt_from_tax
        if billing_address is not None:
            client_data["billingAddress"] = billing_address
        if site_addresses is not None:
            client_data["siteAddresses"] = site_addresses
        if contacts is not None:
            client_data["contacts"] = contacts

        result = await update_client(client_id, client_data)
        return {
            "success": True,
            "data": result,
            "message": f"Client updated successfully. ID: {result}",
        }
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to update client {client_id}: {e}")
        return {"success": False, "error": f"Failed to update client: {str(e)}"}
