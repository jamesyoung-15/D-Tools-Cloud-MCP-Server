"""D-Tools Cloud MCP Tools - Files resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    get_file_details,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_file_info(file_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific file.

    Provides file details including name, URL, and parent object information.

    Args:
        file_id: The unique ID of the file (required).

    Returns:
        Dictionary with success status and file details, or error information.
    """
    try:
        result = await get_file_details(file_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get file {file_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve file: {str(e)}"}
