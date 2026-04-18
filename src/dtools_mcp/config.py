"""Configuration management for D-Tools Cloud MCP Server."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """D-Tools Cloud API configuration from environment variables."""

    dtools_api_key: str = os.getenv("DTOOLS_API_KEY", "")
    dtools_auth_token: str = os.getenv("DTOOLS_AUTH_TOKEN", "")

    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file: str = os.getenv("LOG_FILE", "mcp_server.log")

config = Config()
