"""D-Tools Cloud MCP Server - Entry point."""

import argparse
import logging

import dtools_mcp.logger  # noqa: F401 - initializes logging configuration
from dtools_mcp.tools import mcp

# Configure logging
logger = logging.getLogger(__name__)


def main(transport: str = "stdio") -> None:
    """Start the MCP server.

    Args:
        transport: Transport type - "stdio" (default) or "http"
    """
    logger.info("Starting D-Tools Cloud MCP Server")

    if transport == "http":
        logger.info("Using streamable-http transport")
        mcp.run(transport="streamable-http")
    else:
        logger.info("Using stdio transport")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="D-Tools Cloud MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )

    args = parser.parse_args()
    main(transport=args.transport)
