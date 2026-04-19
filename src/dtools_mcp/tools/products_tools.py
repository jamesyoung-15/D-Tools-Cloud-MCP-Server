"""D-Tools Cloud MCP Tools - Products resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    list_products,
    get_product_details,
    update_product_prices,
    update_product_barcodes,
    update_product_statuses,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


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
async def update_product_price(
    product_id: str,
    msrp: float | None = None,
    unit_cost: float | None = None,
    unit_price: float | None = None,
) -> dict[str, Any]:
    """Update pricing for a specific product in D-Tools Cloud.

    Updates pricing information for a product including MSRP, unit cost, and unit price.

    Args:
        product_id: The UUID of the product to update (required).
        msrp: Manufacturer suggested retail price (optional).
        unit_cost: Unit cost (optional).
        unit_price: Unit price (optional).

    Returns:
        Dictionary with success status and update result, or error details.
    """
    try:
        price_update: dict[str, Any] = {"id": product_id}

        if msrp is not None:
            price_update["msrp"] = msrp
        if unit_cost is not None:
            price_update["unitCost"] = unit_cost
        if unit_price is not None:
            price_update["unitPrice"] = unit_price

        result = await update_product_prices([price_update])
        return {
            "success": True,
            "data": result,
            "message": f"Product price updated successfully. ID: {result}",
        }
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to update product price: {e}")
        return {"success": False, "error": f"Failed to update price: {str(e)}"}


@mcp.tool()
async def update_product_barcode(
    product_id: str,
    upc_barcode: str | None = None,
    ean_barcode: str | None = None,
    itf_barcode: str | None = None,
) -> dict[str, Any]:
    """Update barcodes for a specific product in D-Tools Cloud.

    Updates barcode information for a product including UPC, EAN, and ITF barcodes.

    Args:
        product_id: The UUID of the product to update (required).
        upc_barcode: UPC barcode (optional).
        ean_barcode: EAN barcode (optional).
        itf_barcode: ITF barcode (optional).

    Returns:
        Dictionary with success status and update result, or error details.
    """
    try:
        barcode_update: dict[str, Any] = {"id": product_id}

        if upc_barcode is not None:
            barcode_update["upcBarcode"] = upc_barcode
        if ean_barcode is not None:
            barcode_update["eanBarcode"] = ean_barcode
        if itf_barcode is not None:
            barcode_update["itfBarcode"] = itf_barcode

        result = await update_product_barcodes([barcode_update])
        return {
            "success": True,
            "data": result,
            "message": f"Product barcode updated successfully. ID: {result}",
        }
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to update product barcode: {e}")
        return {"success": False, "error": f"Failed to update barcode: {str(e)}"}


@mcp.tool()
async def update_product_status(
    product_id: str,
    is_active: bool | None = None,
    is_discontinued: bool | None = None,
) -> dict[str, Any]:
    """Update status fields for a specific product in D-Tools Cloud.

    Updates status information for a product including active status and discontinued flag.

    Args:
        product_id: The UUID of the product to update (required).
        is_active: Whether product is active (optional).
        is_discontinued: Whether product is discontinued (optional).

    Returns:
        Dictionary with success status and update result, or error details.
    """
    try:
        status_update: dict[str, Any] = {"id": product_id}

        if is_active is not None:
            status_update["isActive"] = is_active
        if is_discontinued is not None:
            status_update["isDiscontinued"] = is_discontinued

        result = await update_product_statuses([status_update])
        return {
            "success": True,
            "data": result,
            "message": f"Product status updated successfully. ID: {result}",
        }
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to update product status: {e}")
        return {"success": False, "error": f"Failed to update status: {str(e)}"}
