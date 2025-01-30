import os
from functools import lru_cache
from pathlib import Path
from typing import Any, List

import httpx
from decouple import config
from httpx import AsyncClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # App
    TITLE: str = config("TITLE", cast=str, default="Gateway")
    VERSION: str = config("APP_VERSION", cast=str, default="0.0.1")
    TIMEZONE: str = config("TIMEZONE", cast=str, default="UTC")
    DESCRIPTION: str = config("DESCRIPTION", cast=str, default="")

    IS_DEBUG: bool = config("DEBUG", cast=bool, default=False)

    DOCS_URL: str = config("DOCS_URL", cast=str, default='/docs')
    OPENAPI_URL: str = config("OPENAPI_URL", cast=str, default='/redoc')
    REDOC_URL: str = config("REDOC_URL", cast=str, default='/openapi.json')
    OPENAPI_PREFIX: str = config("OPENAPI_PREFIX", cast=str, default="")
    API_PREFIX: str = config("API_PREFIX", cast=str, default="/gateway")

    BASE_DIR: Any = Path(__file__).resolve().parent.parent

    # Logs
    LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="INFO")
    LOG_ROOT: str = os.path.join(BASE_DIR, 'logs/')

    # Server
    HOST: str = config("SERVER_HOST", cast=str)
    PORT: int = config("SERVER_PORT", cast=int)
    WORKERS: int = config("SERVER_WORKERS", cast=int)
    IS_ALLOWED_CREDENTIALS: bool = config("IS_ALLOWED_CREDENTIALS", cast=bool, default=True)
    ALLOWED_HEADER_LIST: List[str] = config(
        "ALLOWED_HEADER_LIST",
        cast=lambda v: [s.strip() for s in v.split(",")],
        default="*"
    )
    ALLOWED_ORIGIN_LIST: List[str] = config(
        "BACKEND_CORS_ORIGINS",
        cast=lambda v: [s.strip() for s in v.split(",")],
        default="*"
    )
    ALLOWED_METHODS: List[str] = config(
        "ALLOWED_METHODS",
        cast=lambda v: [s.strip() for s in v.split(",")],
        default=["GET", "POST"]
    )
    TIMEOUT_SECONDS: int = config("TIMEOUT_SECONDS", cast=int, default=30)

    model_config = SettingsConfigDict(
        env_file=f"{Path().resolve()}/.env",
        case_sensitive=True,
        validate_assignment=True,
        extra="allow",
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
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


settings = AppSettings()

http_client: AsyncClient = httpx.AsyncClient(timeout=settings.TIMEOUT_SECONDS)
