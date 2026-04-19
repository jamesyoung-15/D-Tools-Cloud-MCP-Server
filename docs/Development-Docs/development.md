# Development Guide

## Code Quality

Format code:

```bash
uv run ruff format
```

Check for issues:

```bash
uv run ruff check
```

## Adding New Tools

1. Create endpoint function in `api_endpoints/` directory
2. Export it in `api_endpoints/__init__.py`
3. Add MCP tool in `server.py`
4. Write tests in `tests/` (currently not done, todo later)
5. Update documentation

Example tool:

```python
@mcp.tool()
async def my_new_tool(param1: str) -> dict[str, Any]:
    """Description of what the tool does.

    Args:
        param1: Description of param

    Returns:
        Result dictionary
    """
    try:
        result = await my_endpoint_function(param1)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "error": str(e)}
```

## API Documentation

D-Tools Cloud API Documentation:

- [API Docs](https://docs.d-tools.cloud/en/collections/7640732-cloud-api-documentation)
- [Swagger UI](https://dtcloudapi.d-tools.cloud/apidocs/index.html)

## Adding New API Endpoints

### 1. Create Endpoint File

Create a new file in `src/dtools_mcp/api_endpoints/` following the existing pattern:

```python
# src/dtools_mcp/api_endpoints/new_resource.py
import logging
from typing import Any
from dtools_mcp.shared import BASE_API_URL, get_headers
from dtools_mcp.query_builder import QueryBuilder
import httpx

logger = logging.getLogger(__name__)

async def list_new_resource(
    filter_param: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> Any:
    """List all new resources with optional filtering.

    Args:
        filter_param: Filter by specific field
        page: Page number (default: 1)
        page_size: Items per page (default: 20)

    Returns:
        List of resources

    Raises:
        ValueError: If validation fails
    """
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be positive integers")

    query = (QueryBuilder()
        .add_filter("filterParam", filter_param)
        .add_pagination(page, page_size)
        .build())

    url = f"{BASE_API_URL}/new-resource"
    headers = get_headers()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=query)
        response.raise_for_status()
        return response.json()

async def get_new_resource_details(resource_id: str) -> Any:
    """Get detailed information about a specific resource.

    Args:
        resource_id: The resource ID

    Returns:
        Resource details

    Raises:
        ValueError: If resource_id is empty
    """
    if not resource_id:
        raise ValueError("resource_id is required")

    url = f"{BASE_API_URL}/new-resource/{resource_id}"
    headers = get_headers()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
```

### 2. Export Endpoint Functions

Add to `src/dtools_mcp/api_endpoints/__init__.py`:

```python
from .new_resource import list_new_resource, get_new_resource_details

__all__ = [
    # ... existing exports ...
    "list_new_resource",
    "get_new_resource_details",
]
```

### 3. Add MCP Tools

Add to `src/dtools_mcp/server.py`:

```python
@mcp.tool()
async def get_all_new_resources(
    filter_param: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """List all new resources with optional filtering.

    Args:
        filter_param: Filter by specific field
        page: Page number for pagination (default: 1)
        page_size: Number of items per page (default: 20)

    Returns:
        success: True/False
        data: List of resources
        error: Error message if failed
    """
    try:
        result = await list_new_resource(
            filter_param=filter_param,
            page=page,
            page_size=page_size,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error in get_all_new_resources: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Error fetching new resources: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_new_resource_info(resource_id: str) -> dict[str, Any]:
    """Get detailed information about a specific resource.

    Args:
        resource_id: The resource ID

    Returns:
        success: True/False
        data: Resource details
        error: Error message if failed
    """
    try:
        result = await get_new_resource_details(resource_id)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error in get_new_resource_info: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Error fetching resource {resource_id}: {e}")
        return {"success": False, "error": str(e)}
```

### 4. Write Tests

Create or update `tests/test_mcp_server.py` to validate new tools (currently not done, work in-progress).

### 5. Update Documentation

- Add tool to `docs/features.md` with parameters

## Code Patterns to Follow

### Error Handling

Always use try/except at the tool level:

```python
@mcp.tool()
async def my_tool() -> dict[str, Any]:
    try:
        # Do work
        result = await some_function()
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"success": False, "error": str(e)}
```

### Parameter Validation

Validate early in endpoint functions:

```python
async def list_items(page: int = 1, page_size: int = 20) -> Any:
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be positive integers")
    if page_size > 100:
        raise ValueError("page_size cannot exceed 100")
    # ... rest of function
```

### Query Building

Use QueryBuilder for consistent parameter handling:

```python
query = (QueryBuilder()
    .add_filter("clientId", client_id)
    .add_filter("status", status)
    .add_filter_date_range("createdDate", created_from, created_to)
    .add_search(search_term)
    .add_pagination(page, page_size)
    .add_sort(sort_by, sort_order)
    .build())
```

### Logging

Use centralized logging:

```python
logger = logging.getLogger(__name__)

logger.info(f"Fetching resources with filters: {query}")
logger.error(f"API error: {e}")
logger.debug(f"Response: {response.json()}")
```

## Debugging

Use MCP Inspector to debug tool definitions and calls:

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

This opens an interactive tool tester.

## Testing

See [testing.md](./testing.md).
