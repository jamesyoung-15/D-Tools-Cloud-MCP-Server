"""D-Tools Cloud MCP Tools - Time Entries resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    list_time_entries,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_all_time_entries(
    types: list[str] | None = None,
    resources: list[str] | None = None,
    client_ids: list[str] | None = None,
    project_ids: list[str] | None = None,
    labor_types: list[str] | None = None,
    overtimes_only: bool = False,
    include_archived: bool = False,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all time entries from D-Tools Cloud with optional filtering.

    Supports filtering by type, resource, client, project, and labor type.
    Can search time entries and filter for overtime entries only.

    Args:
        types: Filter by time entry types
        resources: Filter by resources/employees
        client_ids: Filter by client IDs
        project_ids: Filter by project IDs
        labor_types: Filter by labor types
        overtimes_only: Return only overtime entries (default: False)
        include_archived: Include archived entries (default: False)
        search: Search time entries
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and time entries list, or error details.
    """
    try:
        result = await list_time_entries(
            types=types,
            resources=resources,
            client_ids=client_ids,
            project_ids=project_ids,
            labor_types=labor_types,
            overtimes_only=overtimes_only,
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
        logger.error(f"Failed to get time entries: {e}")
        return {"success": False, "error": f"Failed to retrieve time entries: {str(e)}"}
