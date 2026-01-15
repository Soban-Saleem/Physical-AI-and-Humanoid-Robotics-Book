"""
Health check endpoint.

Provides service health status for monitoring and orchestration.
"""

import time
import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.db.qdrant import get_qdrant_service
from app.db.neon import get_neon_service
from app.services.embedding import get_embedding_service
from app.core.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter()

settings = get_settings()


class ServiceStatus(BaseModel):
    """Status of individual services."""

    qdrant: bool = False
    openai: bool = False
    neon: bool = False


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"  # healthy, degraded, unhealthy
    services: dict[str, bool]
    timestamp: int


async def check_qdrant() -> bool:
    """Check Qdrant service health."""
    try:
        qdrant = get_qdrant_service()
        info = await qdrant.collection_info()
        # Collection is healthy if it has a name and dimensions
        return "name" in info and "dimensions" in info and info["dimensions"] > 0
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        return False


async def check_openai() -> bool:
    """Check OpenAI service health."""
    try:
        embedding_service = get_embedding_service()
        # Try a simple embedding generation
        result = await embedding_service.generate_embedding("test")
        return len(result) == 1536  # Expected dimension
    except Exception as e:
        logger.error(f"OpenAI health check failed: {e}")
        return False


async def check_neon() -> bool:
    """Check Neon service health."""
    try:
        neon = get_neon_service()
        if not neon.is_initialized():
            # Neon is optional - degraded but not unhealthy
            return False
        # Try a simple query
        summary = await neon.get_analytics_summary(hours=1)
        return "error" not in summary
    except Exception as e:
        logger.error(f"Neon health check failed: {e}")
        return False


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check health status of all services.

    Returns overall service status and individual service health.
    """
    # Check all services in parallel
    qdrant_status, openai_status, neon_status = await check_all_services()

    # Determine overall status
    services = ServiceStatus(
        qdrant=qdrant_status,
        openai=openai_status,
        neon=neon_status,
    )

    # Overall status logic:
    # - unhealthy: core services (qdrant, openai) are down
    # - degraded: core services up but optional (neon) is down
    # - healthy: all services operational
    if not qdrant_status or not openai_status:
        overall_status = "unhealthy"
    elif not neon_status:
        overall_status = "degraded"
    else:
        overall_status = "healthy"

    return HealthResponse(
        status=overall_status,
        services=services.model_dump(),
        timestamp=int(time.time() * 1000),
    )


async def check_all_services() -> tuple[bool, bool, bool]:
    """
    Check all services in parallel.

    Returns:
        Tuple of (qdrant_status, openai_status, neon_status)
    """
    results = await asyncio_gather(
        check_qdrant(),
        check_openai(),
        check_neon(),
        return_exceptions=True,
    )

    qdrant_status = results[0] if isinstance(results[0], bool) else False
    openai_status = results[1] if isinstance(results[1], bool) else False
    neon_status = results[2] if isinstance(results[2], bool) else False

    return qdrant_status, openai_status, neon_status


# Simple async gather implementation for Python 3.11+
async def asyncio_gather(*coros, return_exceptions=False):
    """Gather coroutines and return results."""
    import asyncio
    return await asyncio.gather(*coros, return_exceptions=return_exceptions)
