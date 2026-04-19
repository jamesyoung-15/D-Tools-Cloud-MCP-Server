"""D-Tools Cloud MCP Tools - Projects resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    get_project_details,
    list_projects,
    update_project,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


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
async def update_existing_project(
    project_id: str,
    name: str | None = None,
    number: str | None = None,
    priority: str | None = None,
    budget: int | None = None,
    salesperson: str | None = None,
    project_manager: str | None = None,
    project_area: int | None = None,
    fulfillment_location: str | None = None,
    opportunity_won_date: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    completed_date: str | None = None,
    billing_address: dict[str, Any] | None = None,
    site_address: dict[str, Any] | None = None,
    contacts: list[dict[str, Any]] | None = None,
    resources: list[str] | None = None,
) -> dict[str, Any]:
    """Update an existing project in D-Tools Cloud.

    Updates the specified fields of an existing project.

    Args:
        project_id: The unique ID of the project to update (required).
        name: Project name.
        number: Project number.
        priority: Project priority level.
        budget: Project budget amount.
        salesperson: Salesperson name or ID.
        project_manager: Project manager name or ID.
        project_area: Project area (int).
        fulfillment_location: Fulfillment location.
        opportunity_won_date: Date opportunity was won (ISO format string).
        start_date: Project start date (ISO format string).
        end_date: Project end date (ISO format string).
        completed_date: Project completion date (ISO format string).
        billing_address: Billing address object with keys: addressLine1, addressLine2, city, state, postalCode, country.
        site_address: Site address object (same structure as billing_address).
        contacts: List of contact objects with keys: name, firstName, lastName, email, phone, etc.
        resources: List of resource names or IDs.

    Returns:
        Dictionary with success status and the updated project UUID, or error details.
    """
    try:
        project_data: dict[str, Any] = {}

        # Add fields to update if provided
        if name is not None:
            project_data["name"] = name
        if number is not None:
            project_data["number"] = number
        if priority is not None:
            project_data["priority"] = priority
        if budget is not None:
            project_data["budget"] = budget
        if salesperson is not None:
            project_data["salesperson"] = salesperson
        if project_manager is not None:
            project_data["projectManager"] = project_manager
        if project_area is not None:
            project_data["projectArea"] = project_area
        if fulfillment_location is not None:
            project_data["fulfillmentLocation"] = fulfillment_location
        if opportunity_won_date is not None:
            project_data["opportunityWonDate"] = opportunity_won_date
        if start_date is not None:
            project_data["startDate"] = start_date
        if end_date is not None:
            project_data["endDate"] = end_date
        if completed_date is not None:
            project_data["completedDate"] = completed_date
        if billing_address is not None:
            project_data["billingAddress"] = billing_address
        if site_address is not None:
            project_data["siteAddress"] = site_address
        if contacts is not None:
            project_data["contacts"] = contacts
        if resources is not None:
            project_data["resources"] = resources

        result = await update_project(project_id, project_data)
        return {
            "success": True,
            "data": result,
            "message": f"Project updated successfully. ID: {result}",
        }
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to update project {project_id}: {e}")
        return {"success": False, "error": f"Failed to update project: {str(e)}"}
