"""D-Tools Cloud MCP Tools - Change Orders resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    list_change_orders,
    get_change_order_details,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_all_change_orders(project_id: str) -> dict[str, Any]:
    """Retrieve all change orders for a specific project.

    Provides a list of change orders associated with a project, showing modifications
    and adjustments made to the project scope and pricing.

    Args:
        project_id: The unique ID of the project (required).

    Returns:
        Dictionary with success status and change orders list, or error details.
    """
    try:
        result = await list_change_orders(project_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get change orders for project {project_id}: {e}")
        return {
            "success": False,
            "error": f"Failed to retrieve change orders: {str(e)}",
        }


@mcp.tool()
async def get_change_order_info(change_order_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific change order.

    Provides comprehensive details about a change order including items, pricing,
    adjustments, payment terms, and status information.

    Args:
        change_order_id: The unique ID of the change order (required).

    Returns:
        Dictionary with success status and change order details, or error information.
    """
    try:
        result = await get_change_order_details(change_order_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get change order {change_order_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve change order: {str(e)}"}
