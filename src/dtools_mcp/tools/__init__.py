"""D-Tools Cloud MCP Tools package."""

# Import all tool modules to register them with the shared mcp instance
from dtools_mcp.tools.shared import mcp
from dtools_mcp.tools import (
    clients_tools,
    projects_tools,
    change_orders_tools,
    opportunities_tools,
    products_tools,
    purchase_orders_tools,
    quotes_tools,
    service_contracts_tools,
    time_entries_tools,
    files_tools,
)

__all__ = [
    "mcp",
    "clients_tools",
    "projects_tools",
    "change_orders_tools",
    "opportunities_tools",
    "products_tools",
    "purchase_orders_tools",
    "quotes_tools",
    "service_contracts_tools",
    "time_entries_tools",
    "files_tools",
]
