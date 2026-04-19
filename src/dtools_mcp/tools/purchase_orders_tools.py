"""D-Tools Cloud MCP Tools - Purchase Orders resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    list_purchase_orders,
    get_purchase_order_details,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_all_purchase_orders(
    suppliers: list[str] | None = None,
    project_ids: list[str] | None = None,
    statuses: list[str] | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all purchase orders from D-Tools Cloud with optional filtering.

    Supports filtering by supplier, project, and status. Can search by supplier
    or purchase order number.

    Args:
        suppliers: Filter by suppliers
        project_ids: Filter by project IDs
        statuses: Filter by purchase order statuses
        search: Search by supplier or PO number
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and purchase orders list, or error details.
    """
    try:
        result = await list_purchase_orders(
            suppliers=suppliers,
            project_ids=project_ids,
            statuses=statuses,
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
        logger.error(f"Failed to get purchase orders: {e}")
        return {
            "success": False,
            "error": f"Failed to retrieve purchase orders: {str(e)}",
        }


@mcp.tool()
async def get_purchase_order_info(purchase_order_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific purchase order.

    Provides comprehensive details about a purchase order including supplier info,
    products, pricing, shipping, and payment information.

    Args:
        purchase_order_id: The unique ID of the purchase order (required).

    Returns:
        Dictionary with success status and purchase order details, or error information.
    """
    try:
        result = await get_purchase_order_details(purchase_order_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get purchase order {purchase_order_id}: {e}")
        return {
            "success": False,
            "error": f"Failed to retrieve purchase order: {str(e)}",
        }
