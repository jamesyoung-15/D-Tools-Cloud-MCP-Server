"""D-Tools Cloud MCP Tools - Opportunities resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    list_opportunities,
    get_opportunity_details,
    create_opportunity,
    update_opportunity,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


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
async def create_new_opportunity(
    name: str,
    client_id: str | None = None,
    client_name: str | None = None,
    type: str | None = None,
    number: str | None = None,
    client_type: str | None = None,
    client_email: str | None = None,
    client_phone: str | None = None,
    associated_project_id: str | None = None,
    building_type: str | None = None,
    market_sector: str | None = None,
    project_type: str | None = None,
    quote_type: str | None = None,
    quote_template: str | None = None,
    priority: str | None = None,
    budget: int | None = None,
    owner: str | None = None,
    project_area: int | None = None,
    fulfillment_location: str | None = None,
    estimated_close_date: str | None = None,
    lead_source: str | None = None,
    billing_address_name: str | None = None,
    billing_address_line1: str | None = None,
    billing_address_line2: str | None = None,
    billing_address_city: str | None = None,
    billing_address_state: str | None = None,
    billing_address_postal_code: str | None = None,
    billing_address_country: str | None = None,
    site_address_name: str | None = None,
    site_address_line1: str | None = None,
    site_address_line2: str | None = None,
    site_address_city: str | None = None,
    site_address_state: str | None = None,
    site_address_postal_code: str | None = None,
    site_address_country: str | None = None,
) -> dict[str, Any]:
    """Create a new opportunity in D-Tools Cloud.

    Creates a new opportunity with the provided details. Requires name and either
    client_id or client_name. Other fields are optional per DTools.Cloud.Data.NewOpportunity schema.

    Args:
        name: The name of the opportunity (required).
        client_id: UUID of the associated client (required if client_name not provided).
        client_name: Name of the client (required if client_id not provided).
        type: Opportunity type (e.g., "Project", "Service").
        number: Opportunity number/reference.
        client_type: Type of client.
        client_email: Client email address.
        client_phone: Client phone number.
        associated_project_id: UUID of associated project.
        building_type: Type of building involved.
        market_sector: Market sector for the opportunity.
        project_type: Type of project.
        quote_type: Type of quote.
        quote_template: Quote template to use.
        priority: Priority level (e.g., "High", "Medium", "Low").
        budget: Budget amount for the opportunity.
        owner: Name of the opportunity owner/manager.
        project_area: Project area (numeric).
        fulfillment_location: Location for fulfillment.
        estimated_close_date: Expected close date (ISO 8601 format).
        lead_source: Source of the lead.
        billing_address_name: Billing address name.
        billing_address_line1: Billing address line 1.
        billing_address_line2: Billing address line 2.
        billing_address_city: Billing address city.
        billing_address_state: Billing address state.
        billing_address_postal_code: Billing address postal code.
        billing_address_country: Billing address country.
        site_address_name: Site address name.
        site_address_line1: Site address line 1.
        site_address_line2: Site address line 2.
        site_address_city: Site address city.
        site_address_state: Site address state.
        site_address_postal_code: Site address postal code.
        site_address_country: Site address country.

    Returns:
        Dictionary with success status and new opportunity ID, or error information.
    """
    try:
        # Validate required parameters
        if not name:
            raise ValueError("name is required")
        if not client_id and not client_name:
            raise ValueError("either client_id or client_name is required")

        opportunity_data: dict[str, Any] = {
            "name": name,
        }

        # Add client info (at least one is required, add both if provided)
        if client_id is not None:
            opportunity_data["clientId"] = client_id
        if client_name is not None:
            opportunity_data["clientName"] = client_name

        # Add optional fields if provided
        if type is not None:
            opportunity_data["type"] = type
        if number is not None:
            opportunity_data["number"] = number
        if client_type is not None:
            opportunity_data["clientType"] = client_type
        if client_email is not None:
            opportunity_data["clientEmail"] = client_email
        if client_phone is not None:
            opportunity_data["clientPhone"] = client_phone
        if associated_project_id is not None:
            opportunity_data["associatedProjectId"] = associated_project_id
        if building_type is not None:
            opportunity_data["buildingType"] = building_type
        if market_sector is not None:
            opportunity_data["marketSector"] = market_sector
        if project_type is not None:
            opportunity_data["projectType"] = project_type
        if quote_type is not None:
            opportunity_data["quoteType"] = quote_type
        if quote_template is not None:
            opportunity_data["quoteTemplate"] = quote_template
        if priority is not None:
            opportunity_data["priority"] = priority
        if budget is not None:
            opportunity_data["budget"] = budget
        if owner is not None:
            opportunity_data["owner"] = owner
        if project_area is not None:
            opportunity_data["projectArea"] = project_area
        if fulfillment_location is not None:
            opportunity_data["fulfillmentLocation"] = fulfillment_location
        if estimated_close_date is not None:
            opportunity_data["estimatedCloseDate"] = estimated_close_date
        if lead_source is not None:
            opportunity_data["leadSource"] = lead_source

        # Build billing address if any address field is provided
        billing_address = {}
        if billing_address_name is not None:
            billing_address["name"] = billing_address_name
        if billing_address_line1 is not None:
            billing_address["addressLine1"] = billing_address_line1
        if billing_address_line2 is not None:
            billing_address["addressLine2"] = billing_address_line2
        if billing_address_city is not None:
            billing_address["city"] = billing_address_city
        if billing_address_state is not None:
            billing_address["state"] = billing_address_state
        if billing_address_postal_code is not None:
            billing_address["postalCode"] = billing_address_postal_code
        if billing_address_country is not None:
            billing_address["country"] = billing_address_country
        if billing_address:
            opportunity_data["billingAddress"] = billing_address

        # Build site address if any address field is provided
        site_address = {}
        if site_address_name is not None:
            site_address["name"] = site_address_name
        if site_address_line1 is not None:
            site_address["addressLine1"] = site_address_line1
        if site_address_line2 is not None:
            site_address["addressLine2"] = site_address_line2
        if site_address_city is not None:
            site_address["city"] = site_address_city
        if site_address_state is not None:
            site_address["state"] = site_address_state
        if site_address_postal_code is not None:
            site_address["postalCode"] = site_address_postal_code
        if site_address_country is not None:
            site_address["country"] = site_address_country
        if site_address:
            opportunity_data["siteAddress"] = site_address

        logger.info(f"Creating opportunity with data: {opportunity_data}")
        result = await create_opportunity(opportunity_data)
        return {"success": True, "data": {"opportunity_id": result}}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to create opportunity: {e}")
        return {"success": False, "error": f"Failed to create opportunity: {str(e)}"}


@mcp.tool()
async def update_existing_opportunity(
    opportunity_id: str,
    name: str | None = None,
    number: str | None = None,
    type: str | None = None,
    client_id: str | None = None,
    associated_project_id: str | None = None,
    building_type: str | None = None,
    market_sector: str | None = None,
    project_type: str | None = None,
    quote_type: str | None = None,
    quote_template: str | None = None,
    priority: str | None = None,
    budget: int | None = None,
    probability: int | None = None,
    owner: str | None = None,
    project_area: int | None = None,
    fulfillment_location: str | None = None,
    estimated_close_date: str | None = None,
    actual_close_date: str | None = None,
    estimated_project_start_date: str | None = None,
    estimated_project_end_date: str | None = None,
    lead_source: str | None = None,
    lost_reason: str | None = None,
    lost_description: str | None = None,
    billing_address_name: str | None = None,
    billing_address_line1: str | None = None,
    billing_address_line2: str | None = None,
    billing_address_city: str | None = None,
    billing_address_state: str | None = None,
    billing_address_postal_code: str | None = None,
    billing_address_country: str | None = None,
    site_address_name: str | None = None,
    site_address_line1: str | None = None,
    site_address_line2: str | None = None,
    site_address_city: str | None = None,
    site_address_state: str | None = None,
    site_address_postal_code: str | None = None,
    site_address_country: str | None = None,
) -> dict[str, Any]:
    """Update an existing opportunity in D-Tools Cloud.

    Updates specified fields of an opportunity. All fields except opportunity_id
    are optional and follow the DTools.Cloud.Data.UpdateOpportunity schema.

    Args:
        opportunity_id: UUID of the opportunity to update (required).
        name: Updated opportunity name.
        number: Updated opportunity number/reference.
        type: Updated opportunity type.
        client_id: Updated associated client UUID.
        associated_project_id: Updated associated project UUID.
        building_type: Updated building type.
        market_sector: Updated market sector.
        project_type: Updated project type.
        quote_type: Updated quote type.
        quote_template: Updated quote template.
        priority: Updated priority level.
        budget: Updated budget amount.
        probability: Updated probability percentage.
        owner: Updated opportunity owner/manager.
        project_area: Updated project area (numeric).
        fulfillment_location: Updated fulfillment location.
        estimated_close_date: Updated close date (ISO 8601 format).
        actual_close_date: Updated actual close date (ISO 8601 format).
        estimated_project_start_date: Updated project start date (ISO 8601 format).
        estimated_project_end_date: Updated project end date (ISO 8601 format).
        lead_source: Updated lead source.
        lost_reason: Reason opportunity was lost.
        lost_description: Description of why opportunity was lost.
        billing_address_name: Billing address name.
        billing_address_line1: Billing address line 1.
        billing_address_line2: Billing address line 2.
        billing_address_city: Billing address city.
        billing_address_state: Billing address state.
        billing_address_postal_code: Billing address postal code.
        billing_address_country: Billing address country.
        site_address_name: Site address name.
        site_address_line1: Site address line 1.
        site_address_line2: Site address line 2.
        site_address_city: Site address city.
        site_address_state: Site address state.
        site_address_postal_code: Site address postal code.
        site_address_country: Site address country.

    Returns:
        Dictionary with success status and updated opportunity ID, or error information.
    """
    try:
        opportunity_data: dict[str, Any] = {}

        # Add fields if provided
        if name is not None:
            opportunity_data["name"] = name
        if number is not None:
            opportunity_data["number"] = number
        if type is not None:
            opportunity_data["type"] = type
        if client_id is not None:
            opportunity_data["clientId"] = client_id
        if associated_project_id is not None:
            opportunity_data["associatedProjectId"] = associated_project_id
        if building_type is not None:
            opportunity_data["buildingType"] = building_type
        if market_sector is not None:
            opportunity_data["marketSector"] = market_sector
        if project_type is not None:
            opportunity_data["projectType"] = project_type
        if quote_type is not None:
            opportunity_data["quoteType"] = quote_type
        if quote_template is not None:
            opportunity_data["quoteTemplate"] = quote_template
        if priority is not None:
            opportunity_data["priority"] = priority
        if budget is not None:
            opportunity_data["budget"] = budget
        if probability is not None:
            opportunity_data["probability"] = probability
        if owner is not None:
            opportunity_data["owner"] = owner
        if project_area is not None:
            opportunity_data["projectArea"] = project_area
        if fulfillment_location is not None:
            opportunity_data["fulfillmentLocation"] = fulfillment_location
        if estimated_close_date is not None:
            opportunity_data["estimatedCloseDate"] = estimated_close_date
        if actual_close_date is not None:
            opportunity_data["actualCloseDate"] = actual_close_date
        if estimated_project_start_date is not None:
            opportunity_data["estimatedProjectStartDate"] = estimated_project_start_date
        if estimated_project_end_date is not None:
            opportunity_data["estimatedProjectEndDate"] = estimated_project_end_date
        if lead_source is not None:
            opportunity_data["leadSource"] = lead_source
        if lost_reason is not None:
            opportunity_data["lostReason"] = lost_reason
        if lost_description is not None:
            opportunity_data["lostDescription"] = lost_description

        # Build billing address if any address field is provided
        billing_address = {}
        if billing_address_name is not None:
            billing_address["name"] = billing_address_name
        if billing_address_line1 is not None:
            billing_address["addressLine1"] = billing_address_line1
        if billing_address_line2 is not None:
            billing_address["addressLine2"] = billing_address_line2
        if billing_address_city is not None:
            billing_address["city"] = billing_address_city
        if billing_address_state is not None:
            billing_address["state"] = billing_address_state
        if billing_address_postal_code is not None:
            billing_address["postalCode"] = billing_address_postal_code
        if billing_address_country is not None:
            billing_address["country"] = billing_address_country
        if billing_address:
            opportunity_data["billingAddress"] = billing_address

        # Build site address if any address field is provided
        site_address = {}
        if site_address_name is not None:
            site_address["name"] = site_address_name
        if site_address_line1 is not None:
            site_address["addressLine1"] = site_address_line1
        if site_address_line2 is not None:
            site_address["addressLine2"] = site_address_line2
        if site_address_city is not None:
            site_address["city"] = site_address_city
        if site_address_state is not None:
            site_address["state"] = site_address_state
        if site_address_postal_code is not None:
            site_address["postalCode"] = site_address_postal_code
        if site_address_country is not None:
            site_address["country"] = site_address_country
        if site_address:
            opportunity_data["siteAddress"] = site_address

        logger.info(
            f"Updating opportunity {opportunity_id} with data: {opportunity_data}"
        )
        result = await update_opportunity(opportunity_id, opportunity_data)
        return {"success": True, "data": {"opportunity_id": result}}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to update opportunity {opportunity_id}: {e}")
        return {"success": False, "error": f"Failed to update opportunity: {str(e)}"}
