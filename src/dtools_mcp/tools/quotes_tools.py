"""D-Tools Cloud MCP Tools - Quotes resource."""

import logging
from typing import Any

from dtools_mcp.api_endpoints import (
    list_quotes,
    get_quote_details,
)
from dtools_mcp.tools.shared import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_all_quotes(opportunity_id: str) -> dict[str, Any]:
    """Retrieve all quotes for a specific opportunity.

    Provides a list of all quotes associated with an opportunity, including
    quote versions, pricing, line items, and status information.

    Args:
        opportunity_id: The unique ID of the opportunity (required).

    Returns:
        Dictionary with success status and quotes list, or error information.
    """
    try:
        if not opportunity_id:
            raise ValueError("opportunity_id is required")
        result = await list_quotes(opportunity_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get quotes for opportunity {opportunity_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve quotes: {str(e)}"}


@mcp.tool()
async def get_quote_info(quote_id: str) -> dict[str, Any]:
    """Retrieve detailed information about a specific quote.

    Provides comprehensive details about a quote including line items, pricing,
    taxes, payment terms, service plans, and file attachments.

    Args:
        quote_id: The unique ID of the quote (required).

    Returns:
        Dictionary with success status and quote details, or error information.
    """
    try:
        result = await get_quote_details(quote_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get quote {quote_id}: {e}")
        return {"success": False, "error": f"Failed to retrieve quote: {str(e)}"}
