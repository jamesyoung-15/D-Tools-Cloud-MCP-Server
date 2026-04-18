from collections.abc import AsyncGenerator
from pprint import pprint

import pytest
from mcp.client.session import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session

from dtools_mcp.server import mcp


@pytest.fixture
async def mcp_client_session() -> AsyncGenerator[ClientSession, None]:
    async with create_connected_server_and_client_session(
        mcp, raise_exceptions=True
    ) as _session:
        yield _session


@pytest.mark.anyio
async def test_mcp_server(mcp_client_session: ClientSession):
    """Test that the MCP server initializes correctly and registers tools."""
    grabbed_tools = await mcp_client_session.list_tools()
    tools = grabbed_tools.tools

    expected_tool_names = {
        "get_all_clients",
        "get_client_info",
        "get_all_projects",
        "get_project_info",
    }
    num_expected_tools = len(expected_tool_names)

    for tool in tools:
        print(f"Registered tool: {tool.name}")
        assert tool.name in expected_tool_names, (
            f"Unexpected tool registered: {tool.name}"
        )

    assert len(tools) == num_expected_tools, (
        f"Expected {num_expected_tools} tools, but got {len(tools)}"
    )
