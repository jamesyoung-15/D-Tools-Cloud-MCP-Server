"""D-Tools Cloud API - Products endpoints."""

import logging
from typing import Any
from datetime import datetime

import httpx

from dtools_mcp.config import config
from dtools_mcp.query_builder import QueryBuilder
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_products(
    brands: list[str] | None = None,
    categories: list[str] | None = None,
    suppliers: list[str] | None = None,
    from_created_date: datetime | None = None,
    to_created_date: datetime | None = None,
    from_modified_date: datetime | None = None,
    to_modified_date: datetime | None = None,
    stock_items_only: bool = False,
    include_inactive: bool = False,
    include_total_count: bool = False,
    search: str | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """Retrieve a list of products from D-Tools Cloud.

    Args:
        brands: Filter by product brands, eg. Apple, Samsung (optional)
        categories: Filter by product categories (optional)
        suppliers: Filter by suppliers (optional)
        from_created_date: Filter by creation date start (optional)
        to_created_date: Filter by creation date end (optional)
        from_modified_date: Filter by modification date start (optional)
        to_modified_date: Filter by modification date end (optional)
        stock_items_only: Return only stock items (default: False)
        include_inactive: Include inactive products (default: False)
        include_total_count: Include total count in response (default: False)
        search: Search products by name/model/brand (optional)
        sort: Sort field (optional)
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        API response containing list of products.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    builder = QueryBuilder("/api/v1/Products/GetProducts")
    builder.add_filters(
        brands=brands,
        categories=categories,
        suppliers=suppliers,
        stockItemsOnly=stock_items_only,
        includeInactive=include_inactive,
        includeTotalCount=include_total_count,
    )
    builder.add_date_range(from_created_date, to_created_date, "Created")
    builder.add_date_range(from_modified_date, to_modified_date, "Modified")
    builder.add_search(search)
    builder.add_sort(sort)
    builder.add_pagination(page, page_size)

    params = builder.build()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Products/GetProducts",
            params=params,
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def get_product_details(product_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific product.

    Args:
        product_id: The UUID of the product to retrieve.

    Returns:
        API response containing product details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not product_id:
        raise ValueError("product_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Products/GetProduct",
            params={"id": product_id},
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def update_product_prices(
    price_updates: list[dict[str, Any]],
) -> str:
    """Update prices for one or more products in D-Tools Cloud.

    Updates pricing information for products including MSRP, unit cost, and unit price.

    Args:
        price_updates: List of price update objects, each containing:
                      - id: Product UUID (required)
                      - msrp: Manufacturer suggested retail price (optional)
                      - unitCost: Unit cost (optional)
                      - unitPrice: Unit price (optional)

    Returns:
        Message indicating successful update.

    Raises:
        ValueError: If price_updates is empty or credentials not configured.
        httpx.HTTPError: If the API request fails.
    """
    if not price_updates:
        raise ValueError("price_updates must contain at least one update")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_API_URL}/Products/UpdateProductPrices",
            json=price_updates,
            headers=get_headers(),
        )

        if response.status_code >= 400:
            logger.error(
                f"Failed to update product prices: "
                f"Status {response.status_code} - {response.text}"
            )
            raise httpx.HTTPStatusError(
                f"API returned status {response.status_code}",
                request=response.request,
                response=response,
            )

        result = response.json()
        logger.info(f"Successfully updated prices for {len(price_updates)} product(s)")
        return result


async def update_product_barcodes(
    barcode_updates: list[dict[str, Any]],
) -> str:
    """Update barcodes for one or more products in D-Tools Cloud.

    Updates barcode information for products including UPC, EAN, and ITF barcodes.

    Args:
        barcode_updates: List of barcode update objects, each containing:
                        - id: Product UUID (required)
                        - upcBarcode: UPC barcode (optional)
                        - eanBarcode: EAN barcode (optional)
                        - itfBarcode: ITF barcode (optional)

    Returns:
        Message indicating successful update.

    Raises:
        ValueError: If barcode_updates is empty or credentials not configured.
        httpx.HTTPError: If the API request fails.
    """
    if not barcode_updates:
        raise ValueError("barcode_updates must contain at least one update")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_API_URL}/Products/UpdateProductBarcodes",
            json=barcode_updates,
            headers=get_headers(),
        )

        if response.status_code >= 400:
            logger.error(
                f"Failed to update product barcodes: "
                f"Status {response.status_code} - {response.text}"
            )
            raise httpx.HTTPStatusError(
                f"API returned status {response.status_code}",
                request=response.request,
                response=response,
            )

        result = response.json()
        logger.info(
            f"Successfully updated barcodes for {len(barcode_updates)} product(s)"
        )
        return result


async def update_product_statuses(
    status_updates: list[dict[str, Any]],
) -> str:
    """Update status fields for one or more products in D-Tools Cloud.

    Updates status information for products including active status and discontinued flag.

    Args:
        status_updates: List of status update objects, each containing:
                       - id: Product UUID (required)
                       - isActive: Whether product is active (optional)
                       - isDiscontinued: Whether product is discontinued (optional)

    Returns:
        Message indicating successful update.

    Raises:
        ValueError: If status_updates is empty or credentials not configured.
        httpx.HTTPError: If the API request fails.
    """
    if not status_updates:
        raise ValueError("status_updates must contain at least one update")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_API_URL}/Products/UpdateProductStatuses",
            json=status_updates,
            headers=get_headers(),
        )

        if response.status_code >= 400:
            logger.error(
                f"Failed to update product statuses: "
                f"Status {response.status_code} - {response.text}"
            )
            raise httpx.HTTPStatusError(
                f"API returned status {response.status_code}",
                request=response.request,
                response=response,
            )

        result = response.json()
        logger.info(
            f"Successfully updated statuses for {len(status_updates)} product(s)"
        )
        return result
