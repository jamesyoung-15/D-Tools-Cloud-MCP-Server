"""D-Tools Cloud MCP Server - Entry point."""

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from dtools_mcp.api_endpoints import (
    get_client_details,
    get_project_details,
    list_clients,
    list_projects,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("D-Tools Cloud")


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
async def get_all_projects(
    client_ids: list[str] | None = None,
    stages: list[str] | None = None,
    stage_groups: list[str] | None = None,
    priorities: list[str] | None = None,
    project_managers: list[str] | None = None,
    search: str | None = None,
    include_archived: bool = False,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all projects from D-Tools Cloud with optional filtering.

    Supports filtering by client, stage, priority, manager, and search terms.

    Args:
        client_ids: Filter by client IDs (e.g., ["client1", "client2"])
        stages: Filter by project stages
        stage_groups: Filter by stage groups
        priorities: Filter by priorities (e.g., ["high", "medium"])
        project_managers: Filter by project manager names
        search: Search by project name or details
        include_archived: Include archived projects (default: False)
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and projects list, or error details.
    """
    try:
        result = await list_projects(
            client_ids=client_ids,
            stages=stages,
            stage_groups=stage_groups,
            priorities=priorities,
            project_managers=project_managers,
            search=search,
            include_archived=include_archived,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get projects: {e}")
        return {"success": False, "error": f"Failed to retrieve projects: {str(e)}"}


@mcp.tool()
async def get_project_info(project_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific project.

    Provides comprehensive details about a project including its status, timeline,
    team members, budget information, and other project-specific data.

    Args:
        project_id: The unique ID of the project (required).

    Returns:
        Dictionary with success status and project details, or error information.
    """
    try:
        result = await get_project_details(project_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get project {project_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve project: {str(e)}"}


def main() -> None:
    """Start the MCP server."""
    logger.info("Starting D-Tools Cloud MCP Server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
