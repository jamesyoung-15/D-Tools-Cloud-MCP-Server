"""MCP Server Tests

Tests cover:
- Tool registration and metadata
- Parameter validation and schema
"""

from collections.abc import AsyncGenerator

import pytest
from mcp.client.session import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session

from dtools_mcp.server import mcp


@pytest.fixture
async def mcp_client_session() -> AsyncGenerator[ClientSession, None]:
    """Create an in-memory MCP client session for testing."""
    async with create_connected_server_and_client_session(
        mcp, raise_exceptions=True
    ) as _session:
        yield _session


class TestToolRegistration:
    """Tests for tool registration and metadata."""

    @pytest.mark.anyio
    async def test_mcp_server_registers_tools(self, mcp_client_session: ClientSession):
        """Test that the MCP server registers tools."""
        tools_request = await mcp_client_session.list_tools()

        assert len(tools_request.tools) > 0, "No tools registered in MCP server"

    @pytest.mark.anyio
    async def test_tool_descriptions_exist(self, mcp_client_session: ClientSession):
        """Test that all tools have descriptions."""
        tools_request = await mcp_client_session.list_tools()
        tools = tools_request.tools

        for tool in tools:
            assert tool.description, f"Tool {tool.name} has no description"
            assert len(tool.description) > 10, (
                f"Tool {tool.name} description is too short"
            )
            print(f"✓ {tool.name}: {tool.description[:60]}...")

    @pytest.mark.anyio
    async def test_list_clients_tool_has_parameters(
        self, mcp_client_session: ClientSession
    ):
        """Test that get_all_clients tool exposes filter parameters."""
        tools_request = await mcp_client_session.list_tools()
        tools = tools_request.tools

        get_all_clients_tool = next(
            (t for t in tools if t.name == "get_all_clients"), None
        )
        assert get_all_clients_tool is not None, "get_all_clients tool not found"

        # Verify tool has input schema with parameters
        input_schema = get_all_clients_tool.inputSchema
        assert "properties" in input_schema, "Tool schema has no properties"

        expected_params = {
            "types",
            "owners",
            "search",
            "include_inactive",
            "page",
            "page_size",
            "sort",
        }
        actual_params = set(input_schema["properties"].keys())
        assert expected_params == actual_params, (
            f"Expected params {expected_params}, got {actual_params}"
        )

        print(f"✓ get_all_clients has all expected parameters: {actual_params}")

    @pytest.mark.anyio
    async def test_list_projects_tool_has_parameters(
        self, mcp_client_session: ClientSession
    ):
        """Test that get_all_projects tool exposes filter parameters."""
        grabbed_tools = await mcp_client_session.list_tools()
        tools = grabbed_tools.tools

        get_all_projects_tool = next(
            (t for t in tools if t.name == "get_all_projects"), None
        )
        assert get_all_projects_tool is not None, "get_all_projects tool not found"

        # Verify tool has input schema with parameters
        input_schema = get_all_projects_tool.inputSchema
        assert "properties" in input_schema, "Tool schema has no properties"

        expected_params = {
            "client_ids",
            "stages",
            "stage_groups",
            "priorities",
            "project_managers",
            "search",
            "include_archived",
            "page",
            "page_size",
            "sort",
        }
        actual_params = set(input_schema["properties"].keys())
        assert expected_params == actual_params, (
            f"Expected params {expected_params}, got {actual_params}"
        )

        print(f"✓ get_all_projects has all expected parameters: {actual_params}")

    @pytest.mark.anyio
    async def test_client_info_tool_has_required_param(
        self, mcp_client_session: ClientSession
    ):
        """Test that get_client_info requires client_id parameter."""
        grabbed_tools = await mcp_client_session.list_tools()
        tools = grabbed_tools.tools

        get_client_info_tool = next(
            (t for t in tools if t.name == "get_client_info"), None
        )
        assert get_client_info_tool is not None, "get_client_info tool not found"

        input_schema = get_client_info_tool.inputSchema
        assert "properties" in input_schema, "Tool schema has no properties"
        assert "client_id" in input_schema["properties"], "client_id parameter missing"
        assert "client_id" in input_schema.get("required", []), (
            "client_id should be required"
        )

        print("✓ get_client_info requires client_id parameter")

    @pytest.mark.anyio
    async def test_project_info_tool_has_required_param(
        self, mcp_client_session: ClientSession
    ):
        """Test that get_project_info requires project_id parameter."""
        grabbed_tools = await mcp_client_session.list_tools()
        tools = grabbed_tools.tools

        get_project_info_tool = next(
            (t for t in tools if t.name == "get_project_info"), None
        )
        assert get_project_info_tool is not None, "get_project_info tool not found"

        input_schema = get_project_info_tool.inputSchema
        assert "properties" in input_schema, "Tool schema has no properties"
        assert "project_id" in input_schema["properties"], (
            "project_id parameter missing"
        )
        assert "project_id" in input_schema.get("required", []), (
            "project_id should be required"
        )

        print("✓ get_project_info requires project_id parameter")

    @pytest.mark.anyio
    async def test_parameter_types_are_correct(self, mcp_client_session: ClientSession):
        """Test that parameters have correct types in the schema."""
        grabbed_tools = await mcp_client_session.list_tools()
        tools = grabbed_tools.tools

        get_all_clients = next((t for t in tools if t.name == "get_all_clients"), None)
        assert get_all_clients is not None, "get_all_clients tool not found"

        schema = get_all_clients.inputSchema["properties"]

        # Verify specific parameter types that have 'type' field
        assert "page" in schema, "page parameter missing"
        assert "page_size" in schema, "page_size parameter missing"
        assert "include_inactive" in schema, "include_inactive parameter missing"
        assert "search" in schema, "search parameter missing"

        if "type" in schema["page"]:
            assert schema["page"]["type"] == "integer", "page should be integer"
        if "type" in schema["page_size"]:
            assert schema["page_size"]["type"] == "integer", (
                "page_size should be integer"
            )
        if "type" in schema["include_inactive"]:
            assert schema["include_inactive"]["type"] == "boolean", (
                "include_inactive should be boolean"
            )

        print("✓ Parameter types are correctly defined")
