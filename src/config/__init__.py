import json
import os
from functools import lru_cache
from os import getenv
from pathlib import Path
from typing import Any

import httpx
from httpx import AsyncClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # App
    TITLE: str = "Gateway"
    VERSION: str = "0.0.1"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str = ""
    IS_DEBUG: bool = False
    BASE_DIR: Any = Path(__file__).resolve().parent.parent

    # Server
    HOST: str = "localhost"
    PORT: int = 8000
    WORKERS: int = 4
    IS_ALLOWED_CREDENTIALS: bool = True
    ALLOWED_HEADERS: str = getenv("ALLOWED_HEADERS", default="*")
    ALLOWED_ORIGINS: str = getenv("ALLOWED_ORIGINS", default="*")
    ALLOWED_METHODS: str = getenv("ALLOWED_METHODS", default="GET, POST, PATCH, PUT, DELETE")
    TIMEOUT_SECONDS: int = 30
    ALLOWED_HEADER_LIST: list[str] = [s.strip() for s in ALLOWED_HEADERS.split(",")]
    ALLOWED_ORIGIN_LIST: list[str] = [s.strip() for s in ALLOWED_ORIGINS.split(",")]
    ALLOWED_METHODS_LIST: list[str] = [s.strip() for s in ALLOWED_METHODS.split(",")]

    # URLS
    API_PREFIX: str = "/api"
    OPENAPI_PREFIX: str = "/api"
    DOCS_URL: str = '/docs'
    OPENAPI_URL: str = '/redoc'
    REDOC_URL: str = '/openapi.json'

    # Logs
    LOG_LEVEL: str = "INFO"
    LOG_ROOT: str = os.path.join(BASE_DIR, 'logs/')

    # Registry file name
    REG_FILE_NAME: str = "registry.json"

    model_config = SettingsConfigDict(
        env_file=f"{Path().resolve()}/.env",
        case_sensitive=True,
        validate_assignment=True,
    )

    @property
    def set_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all FastAPI class' attributes with the custom values defined in BackendBaseSettings.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.IS_DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "root_path": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


settings = AppSettings()

http_client: AsyncClient = httpx.AsyncClient(timeout=settings.TIMEOUT_SECONDS)

api_registry: dict[str, Any] = {}
# load persisted services if file exists
if os.path.exists(settings.REG_FILE_NAME):
    with open(settings.REG_FILE_NAME) as registry_file:
        api_registry = json.load(registry_file)
