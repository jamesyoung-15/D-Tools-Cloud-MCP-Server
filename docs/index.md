# D-Tools Cloud MCP Server

This repo creates a basic Model Context Protocol (MCP) server to allow LLMs to interact with D-Tools Cloud API. For example, with this MCP Server an LLM like Claude can fetch a user's clients, opportunities, projects, etc. from their D-Tool Cloud account.

## Pre-requisites

- [git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Quick Start

- Clone repo

```bash
git clone https://github.com/jamesyoung-15/D-Tools-Cloud-MCP-Server.git
```

- Enter repo

```bash
cd D-Tools-Cloud-MCP-Server
```

- Run server

```bash
uv run main.py
```

## Inspecting/Debugging MCP Server

We can use MCP Inspector tool to test and debug the MCP server:

```bash
npx @modelcontextprotocol/inspector
```

One line to run inspector and MCP server (replace `--directory` argument to point to this repo):

```bash
npx @modelcontextprotocol/inspector uv --directory replace-me run main.py
```
