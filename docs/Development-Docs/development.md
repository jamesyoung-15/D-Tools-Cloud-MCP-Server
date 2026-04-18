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

## Debugging

Use MCP Inspector to debug tool definitions and calls:

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

This opens an interactive tool tester.

## Testing

See [testing.md](./testing.md).
