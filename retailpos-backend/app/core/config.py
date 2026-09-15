from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "RetailPOS API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # SQL Server
    DB_SERVER: str = r"localhost\SQLEXPRESS"
    DB_NAME: str = "RTGW"
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"
    DB_TRUSTED_CONNECTION: bool = True
    DB_USER: str = "sa"
    DB_PASSWORD: str = ""

    # JWT
    JWT_SECRET_KEY: str = Field(
        default="change-me-to-a-long-random-string-in-production",
        min_length=32,
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS – explicit origins only (no wildcards when credentials are used)
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Logging
    LOG_LEVEL: str = "INFO"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> str:
        if isinstance(v, list):
            return ",".join(v)
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def database_url(self) -> str:
        driver = self.DB_DRIVER.replace(" ", "+")
        if self.DB_TRUSTED_CONNECTION:
            return (
                f"mssql+pyodbc://{self.DB_SERVER}/{self.DB_NAME}"
                f"?driver={driver}&trusted_connection=yes&TrustServerCertificate=yes"
            )
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_SERVER}/{self.DB_NAME}"
            f"?driver={driver}&TrustServerCertificate=yes"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()