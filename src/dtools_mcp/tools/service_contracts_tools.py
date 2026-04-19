"""D-Tools Cloud MCP Tools - Service Contracts resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    list_service_contracts,
    get_service_contract_details,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_all_service_contracts(
    client_ids: list[str] | None = None,
    project_ids: list[str] | None = None,
    include_archived: bool = False,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all service contracts from D-Tools Cloud with optional filtering.

    Supports filtering by client, project, and archive status. Can search by
    service contract name or number.

    Args:
        client_ids: Filter by client IDs
        project_ids: Filter by project IDs
        include_archived: Include archived service contracts (default: False)
        search: Search by contract name or number
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and service contracts list, or error details.
    """
    try:
        result = await list_service_contracts(
            client_ids=client_ids,
            project_ids=project_ids,
            include_archived=include_archived,
            search=search,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get service contracts: {e}")
        return {
            "success": False,
            "error": f"Failed to retrieve service contracts: {str(e)}",
        }


@mcp.tool()
async def get_service_contract_info(service_contract_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific service contract.

    Provides comprehensive details about a service contract including client/project info,
    pricing, dates, payment terms, features, and associated files.

    Args:
        service_contract_id: The unique ID of the service contract (required).

    Returns:
        Dictionary with success status and service contract details, or error information.
    """
    try:
        result = await get_service_contract_details(service_contract_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get service contract {service_contract_id}: {e}")
        return {
            "success": False,
            "error": f"Failed to retrieve service contract: {str(e)}",
        }
