# Architecture Overview

## Project Structure

```txt
src/dtools_mcp/
├── config.py              # Configuration (API keys, auth tokens)
├── server.py              # MCP tool definitions
├── query_builder.py       # Query parameter builder
└── api_endpoints/         # Files to call API Endpoints
tests/                     # Tests directory for pytest
```

## Core Components

### Server (server.py)

Exposes MCP tools

### Endpoints

Each file contains API endpoint calls corresponding to their group (eg. `products.py` calls endpoints related to Products as listed in the Swagger).

### Query Builder

Fluent interface for building API parameters:

```python
query = (QueryBuilder()
    .add_search("term")
    .add_pagination(page=1, page_size=20)
    .build())
```

## Data Flow

User Input → MCP Tool → Endpoint Function → QueryBuilder → HTTP Request → D-Tools API → Response

## Authentication

- API Key: Set `DTOOLS_API_KEY` environment variable
- Token: Set `DTOOLS_AUTH_TOKEN` environment variable (fallback)
