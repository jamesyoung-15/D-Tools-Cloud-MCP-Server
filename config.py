from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    dtools_api_key = os.getenv("DTOOLS_API_KEY", "")
    dtools_auth_token = os.getenv("DTOOLS_AUTH_TOKEN", "")


config = Config()
