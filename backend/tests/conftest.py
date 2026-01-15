"""
Pytest configuration and fixtures for RAG chatbot backend tests.
"""

import os
from unittest.mock import AsyncMock, MagicMock
from typing import Generator
import pytest


@pytest.fixture
def mock_qdrant_client() -> MagicMock:
    """Mock Qdrant client for testing."""
    client = MagicMock()
    client.get_collection = MagicMock(return_value=MagicMock(status="green"))
    client.search = MagicMock(return_value=[])
    client.upsert = MagicMock()
    client.create_collection = MagicMock()
    return client


@pytest.fixture
def mock_openai_client() -> MagicMock:
    """Mock OpenAI client for testing."""
    client = MagicMock()
    client.embeddings.create = MagicMock(return_value=MagicMock(data=[MagicMock(embedding=[0.1] * 1536)]))
    client.chat.completions.create = MagicMock(
        return_value=MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )
    )
    return client


@pytest.fixture
def mock_neon_pool() -> MagicMock:
    """Mock Neon Postgres connection pool for testing."""
    pool = MagicMock()
    conn = MagicMock()
    cursor = MagicMock()
    cursor.execute = MagicMock()
    conn.cursor = MagicMock(return_value=cursor)
    pool.connection = MagicMock(return_value=conn)
    return pool


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock environment variables for testing."""
    monkeypatch.setenv("QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("QDRANT_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("NEON_DATABASE_URL", "postgresql://test:test@localhost/test")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000")


@pytest.fixture
async def mock_httpx_client() -> AsyncMock:
    """Mock async HTTP client for external API calls."""
    client = AsyncMock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    return client


@pytest.fixture(autouse=True)
def reset_state() -> None:
    """Reset application state before each test."""
    # Clear any cached modules or singletons
    pass
