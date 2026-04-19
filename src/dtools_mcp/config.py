"""Configuration management for D-Tools Cloud MCP Server."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """D-Tools Cloud MCP Server configuration from environment variables."""

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file: str = os.getenv("LOG_FILE", "mcp_server.log")

    # D-Tools Cloud API
    dtools_api_url: str = os.getenv(
        "DTOOLS_API_URL", "https://dtcloudapi.d-tools.cloud/api/v1"
    )
    dtools_api_key: str = os.getenv("DTOOLS_API_KEY", "")
    dtools_auth_token: str = os.getenv("DTOOLS_AUTH_TOKEN", "")

    # OAuth / Authentication
    enable_auth: bool = os.getenv("ENABLE_AUTH", "true").lower() == "true"
    authentik_issuer: str = os.getenv("AUTHENTIK_ISSUER", "")
    authentik_application: str = os.getenv("AUTHENTIK_APPLICATION", "fastmcp")
    oauth_client_id: str = os.getenv("OAUTH_CLIENT_ID", "")
    oauth_client_secret: str = os.getenv("OAUTH_CLIENT_SECRET", "")
    oauth_base_url: str = os.getenv("OAUTH_BASE_URL", "http://localhost:8000")


config = Config()
