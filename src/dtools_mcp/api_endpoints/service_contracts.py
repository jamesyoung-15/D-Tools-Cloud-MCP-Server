"""D-Tools Cloud API - Service Contracts endpoints."""

import logging
from typing import Any
from datetime import datetime

import httpx

from dtools_mcp.config import config
from dtools_mcp.query_builder import QueryBuilder
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_service_contracts(
    client_ids: list[str] | None = None,
    project_ids: list[str] | None = None,
    from_start_date: datetime | None = None,
    to_start_date: datetime | None = None,
    from_end_date: datetime | None = None,
    to_end_date: datetime | None = None,
    from_payment_due_date: datetime | None = None,
    to_payment_due_date: datetime | None = None,
    from_canceled_date: datetime | None = None,
    to_canceled_date: datetime | None = None,
    from_created_date: datetime | None = None,
    to_created_date: datetime | None = None,
    from_modified_date: datetime | None = None,
    to_modified_date: datetime | None = None,
    include_archived: bool = False,
    include_total_count: bool = False,
    search: str | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """Retrieve a list of service contracts from D-Tools Cloud.

    Args:
        client_ids: Filter by client IDs (optional)
        project_ids: Filter by project IDs (optional)
        from_start_date: Filter by start date start (optional)
        to_start_date: Filter by start date end (optional)
        from_end_date: Filter by end date start (optional)
        to_end_date: Filter by end date end (optional)
        from_payment_due_date: Filter by payment due date start (optional)
        to_payment_due_date: Filter by payment due date end (optional)
        from_canceled_date: Filter by canceled date start (optional)
        to_canceled_date: Filter by canceled date end (optional)
        from_created_date: Filter by creation date start (optional)
        to_created_date: Filter by creation date end (optional)
        from_modified_date: Filter by modification date start (optional)
        to_modified_date: Filter by modification date end (optional)
        include_archived: Include archived service contracts (default: False)
        include_total_count: Include total count in response (default: False)
        search: Search service contracts by name or number (optional)
        sort: Sort field (optional)
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        API response containing list of service contracts.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    builder = QueryBuilder("/api/v1/ServiceContracts/GetServiceContracts")
    builder.add_filters(
        clientIds=client_ids,
        projectIds=project_ids,
        includeArchived=include_archived,
        includeTotalCount=include_total_count,
    )
    builder.add_date_range(from_start_date, to_start_date, "Start")
    builder.add_date_range(from_end_date, to_end_date, "End")
    builder.add_date_range(from_payment_due_date, to_payment_due_date, "PaymentDue")
    builder.add_date_range(from_canceled_date, to_canceled_date, "Canceled")
    builder.add_date_range(from_created_date, to_created_date, "Created")
    builder.add_date_range(from_modified_date, to_modified_date, "Modified")
    builder.add_search(search)
    builder.add_sort(sort)
    builder.add_pagination(page, page_size)

    params = builder.build()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/ServiceContracts/GetServiceContracts",
            params=params,
            headers=get_headers(),
        )
        if response.status_code >= 400:
            logger.error(
                f"Failed to list service contracts: "
                f"Status {response.status_code} - {response.text}"
            )
        response.raise_for_status()
        return response.json()


async def get_service_contract_details(service_contract_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific service contract.

    Args:
        service_contract_id: The UUID of the service contract to retrieve.

    Returns:
        API response containing service contract details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not service_contract_id:
        raise ValueError("service_contract_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/ServiceContracts/GetServiceContract",
            params={"id": service_contract_id},
            headers=get_headers(),
        )
        if response.status_code >= 400:
            logger.error(
                f"Failed to get service contract {service_contract_id}: "
                f"Status {response.status_code} - {response.text}"
            )
        response.raise_for_status()
        return response.json()
