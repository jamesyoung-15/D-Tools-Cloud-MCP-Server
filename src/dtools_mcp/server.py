"""D-Tools Cloud MCP Server - Entry point."""

import logging

import dtools_mcp.logger  # noqa: F401 - initializes logging configuration
from dtools_mcp.tools import mcp

# Configure logging
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the MCP server."""
    logger.info("Starting D-Tools Cloud MCP Server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
