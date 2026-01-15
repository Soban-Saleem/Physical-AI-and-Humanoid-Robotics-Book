"""
Tests for configuration and settings.
"""

import pytest
import os
from unittest.mock import patch

from app.core.config import Settings, get_settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_settings(self):
        """Test that default settings are loaded correctly."""
        # Clear any cached settings
        import app.core.config
        app.core.config._settings = None

        settings = get_settings()

        assert settings.APP_NAME == "RAG Chatbot Backend"
        assert settings.APP_VERSION == "0.1.0"
        assert settings.CHUNK_COUNT == 5
        assert settings.MAX_QUESTION_LENGTH == 5000

    def test_cors_origins_parsing(self, mock_env_vars):
        """Test CORS origins parsing from string."""
        import app.core.config
        app.core.config._settings = None

        settings = Settings(
            CORS_ORIGINS="http://localhost:3000,https://example.com"
        )

        assert len(settings.CORS_ORIGINS) == 2
        assert "http://localhost:3000" in settings.CORS_ORIGINS
        assert "https://example.com" in settings.CORS_ORIGINS

    def test_neon_url_validation(self):
        """Test Neon database URL validation."""
        # Valid URLs
        valid_urls = [
            "postgresql://user:pass@host/db",
            "postgres://user:pass@host/db",
        ]
        for url in valid_urls:
            settings = Settings(NEON_DATABASE_URL=url)
            assert settings.NEON_DATABASE_URL == url

    def test_neon_url_validation_invalid(self):
        """Test Neon URL validation rejects invalid URLs."""
        with pytest.raises(ValueError, match="PostgreSQL connection string"):
            Settings(NEON_DATABASE_URL="invalid://url")

    def test_chunk_count_bounds(self):
        """Test chunk count validation bounds."""
        settings = Settings(CHUNK_COUNT=5)
        assert settings.CHUNK_COUNT == 5

        with pytest.raises(ValueError):
            Settings(CHUNK_COUNT=0)

        with pytest.raises(ValueError):
            Settings(CHUNK_COUNT=15)

    def test_max_question_length_bounds(self):
        """Test max question length validation."""
        settings = Settings(MAX_QUESTION_LENGTH=5000)
        assert settings.MAX_QUESTION_LENGTH == 5000

        with pytest.raises(ValueError):
            Settings(MAX_QUESTION_LENGTH=0)

    def test_debug_mode_default(self):
        """Test that debug mode defaults to False."""
        settings = Settings()
        assert settings.DEBUG is False


class TestEnvironmentLoading:
    """Tests for environment variable loading."""

    def test_qdrant_url_from_env(self, monkeypatch):
        """Test loading QDRANT_URL from environment."""
        monkeypatch.setenv("QDRANT_URL", "http://custom-qdrant:6333")
        import app.core.config
        app.core.config._settings = None

        settings = get_settings()
        assert settings.QDRANT_URL == "http://custom-qdrant:6333"

    def test_openai_key_from_env(self, monkeypatch):
        """Test loading OPENAI_API_KEY from environment."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        import app.core.config
        app.core.config._settings = None

        settings = get_settings()
        assert settings.OPENAI_API_KEY == "sk-test-key-12345"

    def test_multiple_origins_from_env(self, monkeypatch):
        """Test loading CORS_ORIGINS from environment."""
        monkeypatch.setenv(
            "CORS_ORIGINS",
            "http://localhost:3000,https://example.com,https://another.com"
        )
        import app.core.config
        app.core.config._settings = None

        settings = get_settings()
        assert len(settings.CORS_ORIGINS) == 3

    def test_empty_neon_url_allowed(self):
        """Test that empty Neon URL is allowed (analytics optional)."""
        settings = Settings(NEON_DATABASE_URL="")
        assert settings.NEON_DATABASE_URL == ""
