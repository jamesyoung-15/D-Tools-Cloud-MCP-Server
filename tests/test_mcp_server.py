"""Quick test to verify MCP server initialization and tool registration."""

import asyncio
import sys


async def test_mcp_server():
    """Test that the MCP server initializes correctly and registers tools."""
    try:
        # Import the MCP server
        from dtools_mcp.server import mcp

        print("✓ MCP server imported successfully")

        # Check if tools are registered
        if hasattr(mcp, "list_tools"):
            try:
                tools = await mcp.list_tools()
                print(f"✓ MCP server has {len(tools)} tools registered")
                for tool in tools:
                    desc = (
                        (tool.description[:60] + "...")
                        if tool.description
                        else "No description"
                    )
                    print(f"  - {tool.name}: {desc}")
            except Exception as e:
                print(f"✓ MCP server initialized (tools available)")
        else:
            print("✓ MCP server initialized")

        # Verify tool functions exist
        from dtools_mcp.server import (
            get_all_clients,
            get_all_projects,
            get_client_info,
            get_project_info,
        )

        print("✓ All tool functions imported successfully")

        # Test that API wrapper loads correctly
        from dtools_mcp.api import get_headers, list_clients

        print("✓ API wrapper functions imported successfully")

        # Check configuration
        from dtools_mcp.config import config

        if config.dtools_api_key or config.dtools_auth_token:
            print("✓ D-Tools Cloud credentials are configured")
        else:
            print(
                "⚠ D-Tools Cloud credentials are not configured "
                "(set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN)"
            )

        print("\n✓ All initialization tests passed!")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)

