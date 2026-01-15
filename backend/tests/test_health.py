"""
Tests for health check endpoint.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.api.routes.health import (
    health_check,
    check_qdrant,
    check_openai,
    check_neon,
)
from app.models.chat import HealthResponse


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    @pytest.mark.asyncio
    async def test_health_check_all_services_up(
        self,
        mock_qdrant_client,
        mock_openai_client,
    ):
        """Test health check when all services are operational."""
        # Mock Qdrant collection info
        mock_qdrant_client.collection_info = MagicMock(
            return_value={
                "vectors_count": 1000,
                "collection_ready": True,
            }
        )

        # Mock OpenAI embedding
        mock_openai_client.embeddings.create = MagicMock(
            return_value=MagicMock(
                data=[MagicMock(embedding=[0.1] * 1536)]
            )
        )

        with patch(
            "app.api.routes.health.get_qdrant_service",
            return_value=MagicMock(
                collection_info=AsyncMock(
                    return_value={"collection_ready": True}
                )
            )
        ), patch(
            "app.api.routes.health.get_embedding_service",
            return_value=MagicMock(
                generate_embedding=AsyncMock(return_value=[0.1] * 1536)
            )
        ):
            response = await health_check()

            assert response.status == "healthy"
            assert response.services["qdrant"] is True
            assert response.services["openai"] is True
            assert isinstance(response.timestamp, int)

    @pytest.mark.asyncio
    async def test_health_check_qdrant_down(self):
        """Test health check when Qdrant is down."""
        with patch(
            "app.api.routes.health.check_qdrant",
            return_value=False
        ), patch(
            "app.api.routes.health.check_openai",
            return_value=True
        ):
            response = await health_check()

            assert response.status == "unhealthy"
            assert response.services["qdrant"] is False

    @pytest.mark.asyncio
    async def test_health_check_openai_down(self):
        """Test health check when OpenAI is down."""
        with patch(
            "app.api.routes.health.check_openai",
            return_value=False
        ), patch(
            "app.api.routes.health.check_qdrant",
            return_value=True
        ):
            response = await health_check()

            assert response.status == "unhealthy"
            assert response.services["openai"] is False

    @pytest.mark.asyncio
    async def test_health_check_neon_down_degraded(self):
        """Test health check is degraded when only Neon is down."""
        with patch(
            "app.api.routes.health.check_qdrant",
            return_value=True
        ), patch(
            "app.api.routes.health.check_openai",
            return_value=True
        ), patch(
            "app.api.routes.health.check_neon",
            return_value=False
        ):
            response = await health_check()

            assert response.status == "degraded"
            assert response.services["neon"] is False


class TestServiceChecks:
    """Tests for individual service health checks."""

    @pytest.mark.asyncio
    async def test_check_qdrant_healthy(self, mock_qdrant_client):
        """Test Qdrant health check returns True when healthy."""
        with patch(
            "app.db.qdrant.get_qdrant_service",
            return_value=mock_qdrant_client
        ):
            result = await check_qdrant()
            assert result is True

    @pytest.mark.asyncio
    async def test_check_qdrant_unhealthy(self):
        """Test Qdrant health check returns False on error."""
        with patch(
            "app.db.qdrant.get_qdrant_service",
            side_effect=Exception("Connection failed")
        ):
            result = await check_qdrant()
            assert result is False

    @pytest.mark.asyncio
    async def test_check_openai_healthy(self, mock_openai_client):
        """Test OpenAI health check returns True when healthy."""
        with patch(
            "app.services.embedding.get_embedding_service",
            return_value=MagicMock(
                generate_embedding=AsyncMock(return_value=[0.1] * 1536)
            )
        ):
            result = await check_openai()
            assert result is True

    @pytest.mark.asyncio
    async def test_check_openai_unhealthy(self):
        """Test OpenAI health check returns False on error."""
        with patch(
            "app.services.embedding.get_embedding_service",
            return_value=MagicMock(
                generate_embedding=AsyncMock(side_effect=Exception("API Error"))
            )
        ):
            result = await check_openai()
            assert result is False

    @pytest.mark.asyncio
    async def test_check_neon_healthy(self, mock_neon_pool):
        """Test Neon health check returns True when healthy."""
        with patch(
            "app.db.neon.get_neon_service",
            return_value=MagicMock(
                is_initialized=lambda: True,
                get_analytics_summary=AsyncMock(
                    return_value={"total_interactions": 0}
                )
            )
        ):
            result = await check_neon()
            assert result is True

    @pytest.mark.asyncio
    async def test_check_neon_uninitialized(self):
        """Test Neon health check returns False when not initialized."""
        with patch(
            "app.db.neon.get_neon_service",
            return_value=MagicMock(
                is_initialized=lambda: False
            )
        ):
            result = await check_neon()
            assert result is False
