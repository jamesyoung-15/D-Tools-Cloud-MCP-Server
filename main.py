#!/usr/bin/env python
"""Entry point for D-Tools Cloud MCP Server."""

import argparse

from dtools_mcp.server import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the D-Tools Cloud MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mechanism for the MCP server",
    )
    args = parser.parse_args()
    main(transport=args.transport)
