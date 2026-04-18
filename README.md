# D-Tools-Cloud-MCP-Server

Model Context Protocol (MCP) server for D-Tools Cloud API. Enables Claude and other LLMs to interact with D-Tools Cloud resources through natural language.

## Available Tools

Currently supports the following tools:

- get_all_clients
- get_client_info
- get_all_projects
- get_project_info
- get_all_change_orders
- get_change_order_info
- get_all_opportunities
- get_opportunity_info

Working on adding rest of API endpoints.

## Quick Start

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [D-Tools Cloud Account](https://d-tools.cloud/)
- [D-Tools Cloud API Key](https://docs.d-tools.cloud/en/articles/8756116-api-keys-and-webhooks)

### Setup

1. Create `.env` file:

    ```bash
    cp .env.example .env
    ```

2. Configure credentials in `.env`:

    ```env
    DTOOLS_API_KEY=your_api_key
    DTOOLS_AUTH_TOKEN=your_auth_token
    ```

The DTOOLS_AUTH_TOKEN is `RFRDbG91ZEFQSVVzZXI6MyNRdVkrMkR1QCV3Kk15JTU8Yi1aZzlV` as described by their documentation, see [D-Tools Authentication Docs](https://docs.d-tools.cloud/en/articles/8756132-authentication) for details.

### Run Server

```bash
uv run main.py
```

### Debug with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

## References

### MCP Documentation

- [MCP Specification](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/)
- [MCP Inspector Tool](https://modelcontextprotocol.io/docs/tools/inspector)

### D-Tools Cloud API

- [Swagger UI](https://dtcloudapi.d-tools.cloud/apidocs/index.html)
- [Swagger JSON](https://dtcloudapi.d-tools.cloud/swagger/v1/swagger.json)
- [API Documentation](https://docs.d-tools.cloud/en/collections/7640732-cloud-api-documentation)
- [Authentication](https://docs.d-tools.cloud/en/articles/8756132-authentication)
