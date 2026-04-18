""" Logger configuration for D-Tools Cloud MCP Server. """

import logging

from dtools_mcp.config import config

logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.log_file),
        logging.StreamHandler(),
    ],
)