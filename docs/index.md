# D-Tools Cloud MCP Server

This repo creates a basic Model Context Protocol (MCP) server to allow LLMs to interact with D-Tools Cloud API. For example, with this MCP Server an LLM like Claude can fetch a user's clients, opportunities, projects, etc. from their D-Tool Cloud account.

## Pre-requisites

- [git](https://git-scm.com/)
- [D-Tools Cloud Account](https://d-tools.cloud/)
- [D-Tools Cloud API Key](https://docs.d-tools.cloud/en/articles/8756116-api-keys-and-webhooks)
- [Docker Compose](https://docs.docker.com/compose/) or [uv](https://docs.astral.sh/uv/)

## Quick Start

- Clone repo

  ```bash
  git clone https://github.com/jamesyoung-15/D-Tools-Cloud-MCP-Server.git
  ```

- Enter repo

  ```bash
  cd D-Tools-Cloud-MCP-Server
  ```

- Create `.env` file:

  ```bash
  cp .env.example .env
  ```

- Configure D-Tools credentials in `.env`:

  ```env
  DTOOLS_API_KEY=your_api_key
  DTOOLS_AUTH_TOKEN=your_auth_token
  ```

- (Optional) Setup OAuth with Authentik

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

- Run server

  With Docker:

  ```bash
  docker compose up -d
  ```

  With uv (remove `--transport http` for stdio):

  ```bash
  uv run main.py --transport http
  ```

## Inspecting/Debugging MCP Server

You can use MCP Inspector tool to test and debug the MCP server:

```bash
npx @modelcontextprotocol/inspector
```
