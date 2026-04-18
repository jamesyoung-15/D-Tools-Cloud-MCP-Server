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

__all__ = [
    # Clients
    "list_clients",
    "get_client_details",
    # Projects
    "list_projects",
    "get_project_details",
]
