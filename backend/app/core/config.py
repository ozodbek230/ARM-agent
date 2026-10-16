# [Fayl maqsadi: Ilova konfiguratsiyasi va muhit o'zgaruvchilari (pydantic-settings)]
import json
from typing import Annotated, Any
from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_cors_origins(v: Any) -> list[str]:
    if isinstance(v, str):
        v = v.strip()
        if not v:
            return []
        if v.startswith("[") and v.endswith("]"):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed]
            except Exception:
                pass
        return [item.strip() for item in v.split(",") if item.strip()]
    if isinstance(v, (list, tuple, set)):
        return [str(item).strip() for item in v]
    return []


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "ARM - Axborot Resurs Markazi"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = "arm-super-secret-key-change-in-production-at-least-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./arm.db"

    # CORS
    BACKEND_CORS_ORIGINS: Annotated[list[str], BeforeValidator(_parse_cors_origins)] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:5500",
    ]

    # AI Agent
    GEMINI_API_KEY: str = ""
    AI_MODEL: str = "gemini-1.5-flash"


settings = Settings()
