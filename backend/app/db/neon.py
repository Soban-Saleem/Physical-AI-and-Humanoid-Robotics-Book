"""
Neon Postgres client for analytics logging.

Handles connection pooling and interactions with Neon serverless Postgres
for storing anonymized interaction logs.
"""

import logging
from datetime import datetime
from typing import Any, Optional

try:
    from psycopg import ClientCursor
    from psycopg_pool import AsyncConnectionPool
except ImportError:
    ClientCursor = None
    AsyncConnectionPool = None

from app.core.config import get_settings
from app.core.exceptions import ServiceUnavailableException

logger = logging.getLogger(__name__)

# Table name for interaction logs
INTERACTION_LOGS_TABLE = "interaction_logs"


class NeonService:
    """
    Neon Postgres service for analytics.

    Stores anonymized interaction logs for analysis and improvement.
    No PII is stored - all sessions are anonymous.
    """

    def __init__(self) -> None:
        """Initialize the Neon service."""
        self.settings = get_settings()
        self._pool: Optional[AsyncConnectionPool] = None
        self._initialized = False

    def _get_connection_string(self) -> str:
        """
        Get the Neon database connection string.

        Returns:
            str: PostgreSQL connection URL

        Raises:
            ValueError: If database URL is not configured
        """
        if not self.settings.NEON_DATABASE_URL:
            raise ValueError("NEON_DATABASE_URL not configured")
        return self.settings.NEON_DATABASE_URL

    async def initialize_pool(self) -> bool:
        """
        Initialize the async connection pool.

        Returns:
            bool: True if pool is ready for use

        Raises:
            ServiceUnavailableException: If initialization fails
        """
        if not AsyncConnectionPool:
            logger.warning("psycopg not installed - analytics disabled")
            return False

        if not self.settings.NEON_DATABASE_URL:
            logger.info("NEON_DATABASE_URL not configured - analytics disabled")
            return False

        try:
            self._pool = AsyncConnectionPool(
                conninfo=self._get_connection_string(),
                min_size=1,
                max_size=5,
            )

            # Test connection and create table if needed
            async with self._pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(self._get_create_table_sql())
                    await conn.commit()

            logger.info("Neon Postgres connection pool initialized")
            self._initialized = True
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Neon connection pool: {e}")
            self._pool = None
            # Don't raise - analytics is optional
            return False

    def _get_create_table_sql(self) -> str:
        """
        Get SQL for creating the interaction logs table.

        Returns:
            str: SQL CREATE TABLE statement
        """
        return f"""
            CREATE TABLE IF NOT EXISTS {INTERACTION_LOGS_TABLE} (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                question_text TEXT NOT NULL,
                answer_text TEXT,
                citations_count INTEGER DEFAULT 0,
                is_cached BOOLEAN DEFAULT FALSE,
                response_time_ms INTEGER,
                module_id VARCHAR(255),
                error_type VARCHAR(255),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_session_id ON {INTERACTION_LOGS_TABLE}(session_id);
            CREATE INDEX IF NOT EXISTS idx_timestamp ON {INTERACTION_LOGS_TABLE}(timestamp);
            CREATE INDEX IF NOT EXISTS idx_module_id ON {INTERACTION_LOGS_TABLE}(module_id);
        """

    async def log_interaction(
        self,
        session_id: str,
        question: str,
        answer: str | None = None,
        citations_count: int = 0,
        is_cached: bool = False,
        response_time_ms: int | None = None,
        module_id: str | None = None,
        error_type: str | None = None,
    ) -> bool:
        """
        Log an interaction to the database.

        Args:
            session_id: Anonymous session identifier
            question: User's question text
            answer: Chatbot's response (None if error)
            citations_count: Number of citations in response
            is_cached: Whether response was from cache
            response_time_ms: Response time in milliseconds
            module_id: Module ID of cited content
            error_type: Error type if request failed

        Returns:
            bool: True if log was written successfully
        """
        if not self.is_initialized():
            return False

        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        f"""
                        INSERT INTO {INTERACTION_LOGS_TABLE}
                        (session_id, question_text, answer_text, citations_count,
                         is_cached, response_time_ms, module_id, error_type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            session_id,
                            question[:5000],  # Truncate long questions
                            answer[:10000] if answer else None,  # Truncate long answers
                            citations_count,
                            is_cached,
                            response_time_ms,
                            module_id,
                            error_type,
                        ),
                    )
                    await conn.commit()
            return True

        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")
            # Don't raise - analytics failures shouldn't block requests
            return False

    async def get_analytics_summary(
        self,
        hours: int = 24,
    ) -> dict[str, Any]:
        """
        Get analytics summary for the specified time period.

        Args:
            hours: Number of hours to look back

        Returns:
            Dictionary with analytics metrics
        """
        if not self.is_initialized():
            return {"error": "Analytics not available"}

        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        f"""
                        SELECT
                            COUNT(*) as total_interactions,
                            COUNT(CASE WHEN error_type IS NULL THEN 1 END) as successful,
                            COUNT(CASE WHEN is_cached THEN 1 END) as cached,
                            AVG(response_time_ms) as avg_response_time_ms,
                            AVG(citations_count) as avg_citations
                        FROM {INTERACTION_LOGS_TABLE}
                        WHERE timestamp > NOW() - INTERVAL '%s hours'
                        """,
                        (hours,),
                    )
                    result = await cur.fetchone()

                    # Get module breakdown
                    await cur.execute(
                        f"""
                        SELECT module_id, COUNT(*) as count
                        FROM {INTERACTION_LOGS_TABLE}
                        WHERE timestamp > NOW() - INTERVAL '%s hours'
                        AND module_id IS NOT NULL
                        GROUP BY module_id
                        ORDER BY count DESC
                        LIMIT 10
                        """,
                        (hours,),
                    )
                    module_rows = await cur.fetchall()

                    return {
                        "total_interactions": result["total_interactions"],
                        "successful": result["successful"],
                        "cached": result["cached"],
                        "avg_response_time_ms": float(result["avg_response_time_ms"]) if result["avg_response_time_ms"] else None,
                        "avg_citations": float(result["avg_citations"]) if result["avg_citations"] else None,
                        "module_breakdown": [
                            {"module_id": row["module_id"], "count": row["count"]}
                            for row in module_rows
                        ],
                    }

        except Exception as e:
            logger.error(f"Failed to get analytics summary: {e}")
            return {"error": str(e)}

    def is_initialized(self) -> bool:
        """Check if the Neon service is initialized."""
        return self._initialized

    async def close(self) -> None:
        """Close the connection pool."""
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
            self._initialized = False
            logger.info("Neon connection pool closed")


# Global service instance
_neon_service: Optional[NeonService] = None


def get_neon_service() -> NeonService:
    """
    Get the singleton Neon service instance.

    Returns:
        NeonService: Active Neon service (may not be initialized)
    """
    global _neon_service
    if _neon_service is None:
        _neon_service = NeonService()
    return _neon_service
