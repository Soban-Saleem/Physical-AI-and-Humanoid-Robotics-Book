"""
Application configuration using Pydantic Settings.
Loads configuration from environment variables with sensible defaults.
"""

import os
from typing import List
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Qdrant Configuration
    QDRANT_URL: str = Field(
        default="http://localhost:6333",
        description="Qdrant server URL",
    )
    QDRANT_API_KEY: str = Field(
        default="",
        description="Qdrant API key (optional for local instances)",
    )

    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(
        ...,
        description="OpenAI API key for embeddings and chat completions",
    )
    OPENAI_EMBEDDING_MODEL: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model to use",
    )
    OPENAI_CHAT_MODEL: str = Field(
        default="gpt-4o-mini",
        description="OpenAI chat model for response generation",
    )

    # Neon Postgres Configuration
    NEON_DATABASE_URL: str = Field(
        default="",
        description="Neon Postgres connection string for analytics",
    )

    # CORS Configuration
    CORS_ORIGINS: str | List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        description="Allowed CORS origins for the frontend",
    )

    # Application Configuration
    APP_NAME: str = Field(default="RAG Chatbot Backend")
    APP_VERSION: str = Field(default="0.1.0")
    DEBUG: bool = Field(default=False)

    # RAG Configuration
    CHUNK_COUNT: int = Field(default=5, ge=1, le=10, description="Number of chunks to retrieve")
    MAX_QUESTION_LENGTH: int = Field(default=5000, ge=100, description="Max question character length")
    CACHE_TTL_SECONDS: int = Field(default=86400, ge=0, description="Cache TTL in seconds (24 hours)")

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=60, ge=1, description="Requests per minute per session")
    RATE_LIMIT_WINDOW: int = Field(default=60, ge=1, description="Rate limit window in seconds")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @field_validator("NEON_DATABASE_URL")
    @classmethod
    def validate_neon_url(cls, v: str) -> str:
        """Validate Neon database URL format."""
        if v and not v.startswith(("postgresql://", "postgres://")):
            raise ValueError("NEON_DATABASE_URL must be a valid PostgreSQL connection string")
        return v


# Global settings instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """
    Get the application settings instance.
    Creates singleton on first call.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
