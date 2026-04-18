"""D-Tools Cloud API endpoint modules.

Organized by resource type for better code organization and scalability.
"""

from dtools_mcp.api_endpoints.clients import (
    list_clients,
    get_client_details,
)
from dtools_mcp.api_endpoints.projects import (
    list_projects,
    get_project_details,
)
from dtools_mcp.api_endpoints.change_orders import (
    list_change_orders,
    get_change_order_details,
)
from dtools_mcp.api_endpoints.opportunities import (
    list_opportunities,
    get_opportunity_details,
)

__all__ = [
    # Clients
    "list_clients",
    "get_client_details",
    # Projects
    "list_projects",
    "get_project_details",
    # Change Orders
    "list_change_orders",
    "get_change_order_details",
    # Opportunities
    "list_opportunities",
    "get_opportunity_details",
]
