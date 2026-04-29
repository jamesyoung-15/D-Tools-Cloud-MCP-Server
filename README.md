# D-Tools-Cloud-MCP-Server

Model Context Protocol (MCP) server for D-Tools Cloud API. Enables Claude and other LLMs to interact with D-Tools Cloud resources through natural language.

## Overview

### MCP Tools

This MCP server provides 26 tools for accessing D-Tools Cloud resources:

- **Clients**: List clients, get client details, create new client, update existing client
- **Projects**: List projects, get project details, update existing project details
- **Change Orders**: List change orders, get change order details
- **Opportunities**: List opportunities, get opportunity details, create opportunity, update opportunity
- **Products**: List products, get product details, update product prices, update product barcodes, update product status
- **Purchase Orders**: List purchase orders, get purchase order details
- **Quotes**: List quotes for an opportunity, get quote details
- **Service Contracts**: List service contracts, get service contract details
- **Time Entries**: List time entries with filtering
- **Files**: Get file details

All tools support filtering, searching, pagination, and date-range queries where applicable. See [features](./docs/features.md) and D-Tools Cloud [API endpoints](https://dtcloudapi.d-tools.cloud/apidocs/index.html) for more details.

### OAuth

For exposing the MCP server (eg. hosting on VPS), the project supports OAuth to secure the server. Currently only tested with [Authentik](https://goauthentik.io/) with [FastMCP OAuth Proxy](https://gofastmcp.com/servers/auth/oauth-proxy).

## Quick Start

### Prerequisites

- [D-Tools Cloud Account](https://d-tools.cloud/)
- [D-Tools Cloud API Key](https://docs.d-tools.cloud/en/articles/8756116-api-keys-and-webhooks)
- [Docker Compose](https://docs.docker.com/compose/) or [uv](https://docs.astral.sh/uv/)

#### Setup

1. Create `.env` file:

   ```bash
   cp .env.example .env
   ```

2. Configure D-Tools Cloud credentials in `.env`:

   ```env
   DTOOLS_API_KEY=your_api_key
   DTOOLS_AUTH_TOKEN=their_auth_token
   ```

   See [D-Tools Authentication Docs](https://docs.d-tools.cloud/en/articles/8756132-authentication) for details on setting up credentials/auth.

3. (Optional) For setting up OAuth with Authentik for securing MCP server, enable auth and add OAuth config to `.env`:

   ```env
   DTOOLS_API_KEY=your_api_key
   DTOOLS_AUTH_TOKEN=their_auth_token

   ENABLE_AUTH=true
   AUTHENTIK_ISSUER=auth.example.com
   AUTHENTIK_APPLICATION=your_application_name
   OAUTH_BASE_URL=fastmcp.example.com
   OAUTH_CLIENT_ID=yourclientid
   OAUTH_CLIENT_SECRET=yoursecret
   STORAGE_ENCRYPTION_KEY=generatedkey
   ```

   Since this project mainly uses Authentik, it uses [FastMCP OAuth Proxy](https://gofastmcp.com/servers/auth/oauth-proxy). It also uses [file storage](https://gofastmcp.com/servers/storage-backends#file-storage) to persist data. For storage encryption key, generate a Fernet key with something like `uv run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` or use online generator.

### Docker

Quickest way to get project running is through Docker:

```bash
docker compose up -d
```

### Local Dev

#### Run Server

```bash
uv run main.py --transport http
```

Remove the `--transport http` if you want to use `stdio` for dev/debug.

For detailed D-Tools API endpoint documentation and parameters, see [features.md](docs/features.md).

### Debug with MCP Inspector

To quickly test your MCP server, you can use `MCP Inspector`, eg:

```bash
npx @modelcontextprotocol/inspector
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
