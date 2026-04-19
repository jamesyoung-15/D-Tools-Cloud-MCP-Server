"""Shared utilities and FastMCP instance for D-Tools Cloud MCP tools."""

import logging

from mcp.server.fastmcp import FastMCP

# Configure logging
logger = logging.getLogger(__name__)

# Global MCP instance shared across all tool modules
mcp = FastMCP("D-Tools Cloud")
