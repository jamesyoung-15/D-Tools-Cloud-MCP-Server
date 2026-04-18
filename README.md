# D-Tools-Cloud-MCP-Server

Basic MCP server for interacting with D-Tools Cloud API. Currently in development and missing certain API calls.

## Quick Start

Create an `.env` file from the example:

```bash
cp .env.example .env
```

Replace the `DTOOLS_API_KEY` your D-Tools API key and `DTOOLS_AUTH_TOKEN` with auth token from D-Tools' docs ([found here](https://docs.d-tools.cloud/en/articles/8756132-authentication)), eg:

To start the server run `main.py`, eg:

```bash
uv run main.py
```

MCP server can be debugged/tested with MCP inspector, eg:

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

## References

### MCP Server

- [About MCP](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP Python SDK Docs](https://py.sdk.modelcontextprotocol.io/)
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)

### D-Tools Cloud API Docs

- [D-Tools Cloud API Swagger UI](https://dtcloudapi.d-tools.cloud/apidocs/index.html)
- [D-Tools Cloud API Swagger JSON](https://dtcloudapi.d-tools.cloud/swagger/v1/swagger.json)
- [D-Tools Cloud API Docs](https://docs.d-tools.cloud/en/collections/7640732-cloud-api-documentation)
