"""D-Tools Cloud MCP Server - Entry point."""

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from dtools_mcp.api import (
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
async def get_all_clients() -> dict[str, Any]:
    """Retrieve all clients from D-Tools Cloud.

    Returns:
        A list of all available clients with their details.
    """
    try:
        result = await list_clients()
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get clients: {e}")
        return {"success": False, "error": f"Failed to retrieve clients: {str(e)}"}


@mcp.tool()
async def get_client_info(client_id: str) -> dict[str, Any]:
    """Retrieve details for a specific client.

    Args:
        client_id: The ID of the client to retrieve information for.

    Returns:
        Details about the specified client.
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
async def get_all_projects(client_id: str | None = None) -> dict[str, Any]:
    """Retrieve all projects, optionally filtered by client.

    Args:
        client_id: Optional client ID to filter projects by.

    Returns:
        A list of projects matching the query.
    """
    try:
        result = await list_projects(client_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get projects: {e}")
        return {"success": False, "error": f"Failed to retrieve projects: {str(e)}"}


@mcp.tool()
async def get_project_info(project_id: str) -> dict[str, Any]:
    """Retrieve details for a specific project.

    Args:
        project_id: The ID of the project to retrieve information for.

    Returns:
        Details about the specified project.
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
