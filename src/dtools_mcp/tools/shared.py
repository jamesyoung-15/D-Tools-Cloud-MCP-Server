"""Shared utilities and FastMCP instance for D-Tools Cloud MCP tools."""

import logging

from fastmcp import FastMCP
from fastmcp.server.auth import OAuthProxy
from fastmcp.server.auth.providers.jwt import JWTVerifier
from key_value.aio.stores.disk import DiskStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

from dtools_mcp.config import config

# Configure logging
logger = logging.getLogger(__name__)

# Initialize auth based on configuration
auth = None

if config.enable_auth:
    if not config.oauth_client_secret:
        logger.warning(
            "enable_auth=true but OAUTH_CLIENT_SECRET not set - disabling auth"
        )
    else:
        # Token verifier for validating OAuth tokens from Authentik
        token_verifier = JWTVerifier(
            jwks_uri=f"{config.authentik_issuer}/application/o/{config.authentik_application}/jwks/",
            issuer=f"{config.authentik_issuer}/application/o/{config.authentik_application}/",
            audience=config.oauth_client_id,
        )

        # OAuth Proxy for DCR-enabled clients (like MCP Inspector)
        auth = OAuthProxy(
            upstream_authorization_endpoint=f"{config.authentik_issuer}/application/o/authorize/",
            upstream_token_endpoint=f"{config.authentik_issuer}/application/o/token/",
            upstream_client_id=config.oauth_client_id,
            upstream_client_secret=config.oauth_client_secret,
            token_verifier=token_verifier,
            base_url=config.oauth_base_url,
            client_storage=FernetEncryptionWrapper(
                key_value=DiskStore(directory=config.auth_storage_path),
                fernet=Fernet(config.storage_encryption_key.encode()),
            ),
        )

        logger.info("OAuth authentication enabled")
        logger.info(f"  Issuer: {config.authentik_issuer}")
        logger.info(f"  Client ID: {config.oauth_client_id}")
else:
    logger.info("OAuth authentication disabled")

# FastMCP server with optional OAuth
mcp = FastMCP(name="D-Tools Cloud", auth=auth)
