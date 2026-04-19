"""D-Tools Cloud API - Projects endpoints."""

import logging
from typing import Any
from datetime import datetime

import httpx

from dtools_mcp.config import config
from dtools_mcp.query_builder import QueryBuilder
from dtools_mcp.api_endpoints.shared import BASE_API_URL, get_headers

logger = logging.getLogger(__name__)


async def list_projects(
    client_ids: list[str] | None = None,
    stage_groups: list[str] | None = None,
    stages: list[str] | None = None,
    priorities: list[str] | None = None,
    project_managers: list[str] | None = None,
    from_start_date: datetime | None = None,
    to_start_date: datetime | None = None,
    from_end_date: datetime | None = None,
    to_end_date: datetime | None = None,
    from_completed_date: datetime | None = None,
    to_completed_date: datetime | None = None,
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
    """Retrieve a list of projects from D-Tools Cloud.

    Args:
        client_ids: Filter by client IDs (optional)
        stage_groups: Filter by stage groups (optional)
        stages: Filter by stages (optional)
        priorities: Filter by priorities (optional)
        project_managers: Filter by project manager names (optional)
        from_start_date: Filter by start date beginning (optional)
        to_start_date: Filter by start date ending (optional)
        from_end_date: Filter by end date beginning (optional)
        to_end_date: Filter by end date ending (optional)
        from_completed_date: Filter by completion date beginning (optional)
        to_completed_date: Filter by completion date ending (optional)
        from_created_date: Filter by creation date beginning (optional)
        to_created_date: Filter by creation date ending (optional)
        from_modified_date: Filter by modification date beginning (optional)
        to_modified_date: Filter by modification date ending (optional)
        include_archived: Include archived projects (default: False)
        include_total_count: Include total count in response (default: False)
        search: Search projects by name/number (optional)
        sort: Sort field (optional)
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        API response containing list of projects.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured.
    """
    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    builder = QueryBuilder("/api/v1/Projects/GetProjects")
    builder.add_filters(
        clientIds=client_ids,
        stageGroups=stage_groups,
        stages=stages,
        priorities=priorities,
        projectManagers=project_managers,
        includeArchived=include_archived,
        includeTotalCount=include_total_count,
    )
    builder.add_date_range(from_start_date, to_start_date, "Start")
    builder.add_date_range(from_end_date, to_end_date, "End")
    builder.add_date_range(from_completed_date, to_completed_date, "Completed")
    builder.add_date_range(from_created_date, to_created_date, "Created")
    builder.add_date_range(from_modified_date, to_modified_date, "Modified")
    builder.add_search(search)
    builder.add_sort(sort)
    builder.add_pagination(page, page_size)

    params = builder.build()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Projects/GetProjects",
            params=params,
            headers=get_headers(),
        )
        if response.status_code >= 400:
            logger.error(
                f"Failed to list projects: "
                f"Status {response.status_code} - {response.text}"
            )
        response.raise_for_status()
        return response.json()


async def get_project_details(project_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific project.

    Args:
        project_id: The UUID of the project to retrieve.

    Returns:
        API response containing project details.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not project_id:
        raise ValueError("project_id is required")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_API_URL}/Projects/GetProject",
            params={"id": project_id},
            headers=get_headers(),
        )
        if response.status_code >= 400:
            logger.error(
                f"Failed to get project {project_id}: "
                f"Status {response.status_code} - {response.text}"
            )
        response.raise_for_status()
        return response.json()


async def update_project(project_id: str, project_data: dict[str, Any]) -> str:
    """Update an existing project in D-Tools Cloud.

    Args:
        project_id: The UUID of the project to update.
        project_data: Dictionary containing project fields to update.
            Updateable fields: clientId, name, number, priority, budget,
                             salesperson, projectManager, projectArea,
                             fulfillmentLocation, opportunityWonDate,
                             startDate, endDate, completedDate,
                             billingAddress, siteAddress, contacts, resources, etc.

            Address object structure (billingAddress, siteAddress):
            {
                "name": str (optional),
                "addressLine1": str,
                "addressLine2": str (optional),
                "city": str,
                "state": str,
                "postalCode": str,
                "country": str
            }

            Contact object structure (contacts array):
            {
                "id": str (optional UUID),
                "name": str,
                "firstName": str,
                "lastName": str,
                "company": str (optional),
                "title": str (optional),
                "email": str,
                "secondaryEmail": str (optional),
                "mobile": str (optional),
                "phone": str (optional),
                "fax": str (optional),
                "addressLine1": str (optional),
                "addressLine2": str (optional),
                "city": str (optional),
                "state": str (optional),
                "postalCode": str (optional),
                "country": str (optional),
                "notes": str (optional),
                "isActive": bool (optional),
                "isPrimary": bool (optional)
            }

    Returns:
        The UUID of the updated project.

    Raises:
        httpx.HTTPError: If the API request fails.
        ValueError: If authentication is not configured or ID is invalid.
    """
    if not project_id:
        raise ValueError("project_id is required")

    if not project_data:
        raise ValueError("project_data must contain at least one field to update")

    if not config.dtools_api_key and not config.dtools_auth_token:
        raise ValueError(
            "D-Tools credentials not configured. "
            "Set DTOOLS_API_KEY or DTOOLS_AUTH_TOKEN environment variables."
        )

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_API_URL}/Projects/UpdateProject",
            params={"id": project_id},
            json=project_data,
            headers=get_headers(),
        )
        if response.status_code >= 400:
            error_details = response.text
            try:
                error_json = response.json()
                error_details = error_json
            except Exception:
                pass
            logger.error(f"API Error: {response.status_code} - {error_details}")
            response.raise_for_status()
        return response.json()
