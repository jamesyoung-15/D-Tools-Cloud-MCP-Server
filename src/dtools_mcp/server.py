"""D-Tools Cloud MCP Server - Entry point."""

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

import dtools_mcp.logger  # noqa: F401 - initializes logging configuration
from dtools_mcp.config import config
from dtools_mcp.api_endpoints import (
    get_client_details,
    get_project_details,
    list_clients,
    list_projects,
    list_change_orders,
    get_change_order_details,
    list_opportunities,
    get_opportunity_details,
    list_products,
    get_product_details,
    list_purchase_orders,
    get_purchase_order_details,
)

# Configure logging
logger = logging.getLogger(__name__)

mcp = FastMCP("D-Tools Cloud")


@mcp.tool()
async def get_all_clients(
    types: list[str] | None = None,
    owners: list[str] | None = None,
    search: str | None = None,
    include_inactive: bool = False,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all clients from D-Tools Cloud with optional filtering.

    Supports filtering by type, owner, search terms, and date ranges.

    Args:
        types: Filter by client types (e.g., ["Business", "Individual"])
        owners: Filter by owner names
        search: Search by client name or details
        include_inactive: Include inactive clients (default: False)
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and client list, or error details.
    """
    try:
        result = await list_clients(
            types=types,
            owners=owners,
            search=search,
            include_inactive=include_inactive,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get clients: {e}")
        return {"success": False, "error": f"Failed to retrieve clients: {str(e)}"}


@mcp.tool()
async def get_client_info(client_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific client.

    Provides comprehensive details about a client including their contact information,
    address, client type, and modification history.

    Args:
        client_id: The unique ID of the client (required).

    Returns:
        Dictionary with success status and client details, or error information.
    """
    try:
        result = await get_client_details(client_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get client {client_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve client: {str(e)}"}


@mcp.tool()
async def get_all_projects(
    client_ids: list[str] | None = None,
    stages: list[str] | None = None,
    stage_groups: list[str] | None = None,
    priorities: list[str] | None = None,
    project_managers: list[str] | None = None,
    search: str | None = None,
    include_archived: bool = False,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all projects from D-Tools Cloud with optional filtering.

    Supports filtering by client, stage, priority, manager, and search terms.

    Args:
        client_ids: Filter by client IDs (e.g., ["client1", "client2"])
        stages: Filter by project stages
        stage_groups: Filter by stage groups
        priorities: Filter by priorities (e.g., ["high", "medium"])
        project_managers: Filter by project manager names
        search: Search by project name or details
        include_archived: Include archived projects (default: False)
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and projects list, or error details.
    """
    try:
        result = await list_projects(
            client_ids=client_ids,
            stages=stages,
            stage_groups=stage_groups,
            priorities=priorities,
            project_managers=project_managers,
            search=search,
            include_archived=include_archived,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get projects: {e}")
        return {"success": False, "error": f"Failed to retrieve projects: {str(e)}"}


@mcp.tool()
async def get_project_info(project_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific project.

    Provides comprehensive details about a project including its status, timeline,
    team members, budget information, and other project-specific data.

    Args:
        project_id: The unique ID of the project (required).

    Returns:
        Dictionary with success status and project details, or error information.
    """
    try:
        result = await get_project_details(project_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get project {project_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve project: {str(e)}"}


@mcp.tool()
async def get_all_change_orders(project_id: str) -> dict[str, Any]:
    """Retrieve all change orders for a specific project.

    Provides a list of change orders associated with a project, showing modifications
    and adjustments made to the project scope and pricing.

    Args:
        project_id: The unique ID of the project (required).

    Returns:
        Dictionary with success status and change orders list, or error details.
    """
    try:
        result = await list_change_orders(project_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get change orders for project {project_id}: {e}")
        return {
            "success": False,
            "error": f"Failed to retrieve change orders: {str(e)}",
        }


@mcp.tool()
async def get_change_order_info(change_order_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific change order.

    Provides comprehensive details about a change order including items, pricing,
    adjustments, payment terms, and status information.

    Args:
        change_order_id: The unique ID of the change order (required).

    Returns:
        Dictionary with success status and change order details, or error information.
    """
    try:
        result = await get_change_order_details(change_order_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get change order {change_order_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve change order: {str(e)}"}


@mcp.tool()
async def get_all_opportunities(
    types: list[str] | None = None,
    client_ids: list[str] | None = None,
    stages: list[str] | None = None,
    stage_groups: list[str] | None = None,
    priorities: list[str] | None = None,
    owners: list[str] | None = None,
    search: str | None = None,
    include_archived: bool = False,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all opportunities from D-Tools Cloud with optional filtering.

    Supports filtering by type, client, stage, priority, owner, and search terms.

    Args:
        types: Filter by opportunity types
        client_ids: Filter by client IDs (e.g., ["client1", "client2"])
        stages: Filter by opportunity stages
        stage_groups: Filter by stage groups
        priorities: Filter by priorities (e.g., ["high", "medium"])
        owners: Filter by owner names
        search: Search by opportunity name or details
        include_archived: Include archived opportunities (default: False)
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and opportunities list, or error details.
    """
    try:
        result = await list_opportunities(
            types=types,
            client_ids=client_ids,
            stages=stages,
            stage_groups=stage_groups,
            priorities=priorities,
            owners=owners,
            search=search,
            include_archived=include_archived,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get opportunities: {e}")
        return {
            "success": False,
            "error": f"Failed to retrieve opportunities: {str(e)}",
        }


@mcp.tool()
async def get_opportunity_info(opportunity_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific opportunity.

    Provides comprehensive details about an opportunity including client information,
    pricing, stage, probability, and associated quotes and resources.

    Args:
        opportunity_id: The unique ID of the opportunity (required).

    Returns:
        Dictionary with success status and opportunity details, or error information.
    """
    try:
        result = await get_opportunity_details(opportunity_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get opportunity {opportunity_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve opportunity: {str(e)}"}


@mcp.tool()
async def get_all_products(
    brands: list[str] | None = None,
    categories: list[str] | None = None,
    suppliers: list[str] | None = None,
    stock_items_only: bool = False,
    include_inactive: bool = False,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all products from D-Tools Cloud with optional filtering.

    Supports filtering by brand, category, supplier, and search terms.
    Can filter for stock items only or include inactive products.

    Args:
        brands: Filter by product brands
        categories: Filter by product categories
        suppliers: Filter by suppliers
        stock_items_only: Return only stock items (default: False)
        include_inactive: Include inactive products (default: False)
        search: Search by product name, model, or brand
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and products list, or error details.
    """
    try:
        result = await list_products(
            brands=brands,
            categories=categories,
            suppliers=suppliers,
            stock_items_only=stock_items_only,
            include_inactive=include_inactive,
            search=search,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get products: {e}")
        return {"success": False, "error": f"Failed to retrieve products: {str(e)}"}


@mcp.tool()
async def get_product_info(product_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific product.

    Provides comprehensive details about a product including pricing, specifications,
    images, labor items, accessories, subscriptions, and inventory information.

    Args:
        product_id: The unique ID of the product (required).

    Returns:
        Dictionary with success status and product details, or error information.
    """
    try:
        result = await get_product_details(product_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get product {product_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve product: {str(e)}"}


@mcp.tool()
async def get_all_purchase_orders(
    suppliers: list[str] | None = None,
    project_ids: list[str] | None = None,
    statuses: list[str] | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str | None = None,
) -> dict[str, Any]:
    """Retrieve all purchase orders from D-Tools Cloud with optional filtering.

    Supports filtering by supplier, project, and status. Can search by supplier
    or purchase order number.

    Args:
        suppliers: Filter by suppliers
        project_ids: Filter by project IDs
        statuses: Filter by purchase order statuses
        search: Search by supplier or PO number
        page: Page number for pagination (default: 1)
        page_size: Items per page (default: 20, max: 100)
        sort: Sort field name

    Returns:
        Dictionary with success status and purchase orders list, or error details.
    """
    try:
        result = await list_purchase_orders(
            suppliers=suppliers,
            project_ids=project_ids,
            statuses=statuses,
            search=search,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get purchase orders: {e}")
        return {"success": False, "error": f"Failed to retrieve purchase orders: {str(e)}"}


@mcp.tool()
async def get_purchase_order_info(purchase_order_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific purchase order.

    Provides comprehensive details about a purchase order including supplier info,
    products, pricing, shipping, and payment information.

    Args:
        purchase_order_id: The unique ID of the purchase order (required).

    Returns:
        Dictionary with success status and purchase order details, or error information.
    """
    try:
        result = await get_purchase_order_details(purchase_order_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get purchase order {purchase_order_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve purchase order: {str(e)}"}


def main() -> None:
    """Start the MCP server."""
    logger.info("Starting D-Tools Cloud MCP Server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
