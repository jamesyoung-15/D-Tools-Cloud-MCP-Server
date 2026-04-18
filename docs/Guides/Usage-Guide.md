# Using the MCP Server with AI Agents

This guide explains how to use the D-Tools Cloud MCP server with Claude and other LLMs.

## Claude Desktop

See [setup guide](./claude-desktop-mcp-setup.md).

### Usage Patterns

Ask Claude about D-Tools resources naturally:

```text
"Show me all active projects for client ABC"
↓
Claude selects get_all_projects() with filters
↓
Returns filtered project list
```

```text
"Get details for opportunity #12345"
↓
Claude selects get_opportunity_info(opportunity_id)
↓
Returns full opportunity data
```

```text
"List purchase orders from supplier XYZ received in March"
↓
Claude selects get_all_purchase_orders() with date and supplier filters
↓
Returns matching POs with details
```

## MCP Inspector (Development)

Test tools interactively without Claude:

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

This opens a web UI where you can:

- See all available tools
- Call tools with test parameters
- View responses and errors
- Debug parameter schemas

## Using with Other LLM Clients

Any client supporting the MCP specification can connect:

- **OpenAI GPT-4 with custom tools** - Implement MCP ↔ OpenAI adapter
- **Anthropic API direct** - Use FastMCP's HTTP transport (see [FastMCP docs](https://docs.fastmcp.dev/docs/implementations))
- **Other MCP clients** - Connect via stdio, SSE, or HTTP

## Best Practices

### 1. Provide Context

Give Claude enough information to construct accurate queries:

```text
❌ "Show me orders"
✅ "Show me all purchase orders for project 'BuildingSystems' from March through May, sorted by date"
```

### 2. Use Natural Language

Claude understands filters implicitly:

```text
"Archived projects" → includes include_archived filter
"Recently created" → sorts by creation date descending
"Search for 'electrical'" → applies search filter
```

### 3. Handle Large Datasets

The tools support pagination. Claude can request next pages:

```text
"Show me 50 results per page, page 2"
↓
Calls get_all_clients(page=2, page_size=50)
```

### 4. Combine Operations

Claude chains multiple tool calls:

```text
"For opportunity #999, get the opportunity details and all associated quotes"
↓
1. Calls get_opportunity_info(999)
2. Calls get_all_quotes(opportunity_id=999)
3. Combines and presents results
```

## Error Handling

All tools return consistent responses:

```json
{
  "success": true,
  "data": { /* API response */ }
}
```

or

```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

Common errors:

- `DTOOLS_API_KEY` or `DTOOLS_AUTH_TOKEN` not set → Set credentials in `.env` or Claude config
- Invalid parameters → Claude typically corrects automatically
- API errors → Check D-Tools API status or credentials validity

## Rate Limiting

The D-Tools API has rate limits. When Claude receives rate limit errors:

- It will pause and retry (automatic exponential backoff)
- Break large queries into smaller chunks if needed

## Debugging

1. **Check MCP Inspector** - Verify tools are registered correctly
2. **Check logs** - Review `server.log` for detailed error messages
3. **Test with curl** - Verify D-Tools API credentials work:

    ```bash
    curl -H "Authorization: Bearer $DTOOLS_AUTH_TOKEN" \
         https://dtcloudapi.d-tools.cloud/v1/clients
    ```

4. **Enable debug logging** - Set `LOG_LEVEL=DEBUG` in `.env`
