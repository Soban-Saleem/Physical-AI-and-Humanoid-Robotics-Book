"""
Shared dependency injection for API routes.

Provides common dependencies like rate limiting, session management,
and request validation.
"""

import hashlib
import secrets
import time
from typing import Annotated, Optional

from fastapi import Header, HTTPException, Request, status
from pydantic import BaseModel, Field, validator

from app.core.config import get_settings

settings = get_settings()


# =============================================================================
# Rate Limiting
# =============================================================================


class RateLimiter:
    """
    Simple in-memory rate limiter.

    Uses a sliding window approach per session ID.
    For production, consider Redis-backed rate limiting.
    """

    def __init__(self) -> None:
        """Initialize the rate limiter."""
        self._requests: dict[str, list[float]] = {}

    def is_allowed(
        self,
        session_id: str,
        limit: int,
        window: int,
    ) -> bool:
        """
        Check if a request is allowed under rate limits.

        Args:
            session_id: Session identifier
            limit: Maximum requests per window
            window: Time window in seconds

        Returns:
            bool: True if request is allowed
        """
        now = time.time()
        window_start = now - window

        # Get existing timestamps for this session
        timestamps = self._requests.get(session_id, [])

        # Filter timestamps outside the window
        recent = [ts for ts in timestamps if ts > window_start]

        # Check if limit exceeded
        if len(recent) >= limit:
            return False

        # Add current request
        recent.append(now)
        self._requests[session_id] = recent

        return True

    def get_retry_after(
        self,
        session_id: str,
        window: int,
    ) -> int:
        """
        Calculate seconds until next request is allowed.

        Args:
            session_id: Session identifier
            window: Time window in seconds

        Returns:
            int: Seconds until retry
        """
        timestamps = self._requests.get(session_id, [])
        if not timestamps:
            return 0

        oldest = min(timestamps)
        retry_at = oldest + window
        now = time.time()
        return max(0, int(retry_at - now))


# Global rate limiter instance
_rate_limiter = RateLimiter()


async def check_rate_limit(
    request: Request,
    x_session_id: Annotated[
        Optional[str],
        Header(alias="X-Session-ID")
    ] = None,
) -> str:
    """
    Dependency to check rate limits for incoming requests.

    Args:
        request: FastAPI request object
        x_session_id: Optional session ID from header

    Returns:
        str: Session ID (existing or generated)

    Raises:
        HTTPException: If rate limit exceeded
    """
    # Use existing session ID or generate new one
    session_id = x_session_id or secrets.token_urlsafe(16)

    # Check rate limit
    if not _rate_limiter.is_allowed(
        session_id,
        settings.RATE_LIMIT_REQUESTS,
        settings.RATE_LIMIT_WINDOW,
    ):
        retry_after = _rate_limiter.get_retry_after(
            session_id,
            settings.RATE_LIMIT_WINDOW,
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "RateLimitExceeded",
                "message": f"Rate limit exceeded. Try again in {retry_after} seconds.",
                "retry_after": retry_after,
            },
        )

    return session_id


# =============================================================================
# Request Validation
# =============================================================================


class QuestionValidator(BaseModel):
    """Validate incoming question text."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_QUESTION_LENGTH,
        description="User's question text",
    )

    @validator("question")
    def question_not_empty(cls, v: str) -> str:
        """Ensure question is not just whitespace."""
        if not v.strip():
            raise ValueError("Question cannot be empty or whitespace only")
        return v.strip()


class SelectedTextValidator(BaseModel):
    """Validate selected text for text-selection mode."""

    selected_text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Selected text from the page",
    )
    page_url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="URL of the page with selection",
    )

    @validator("selected_text")
    def selection_not_empty(cls, v: str) -> str:
        """Ensure selection is not just whitespace."""
        if not v.strip():
            raise ValueError("Selected text cannot be empty or whitespace only")
        return v.strip()

    @validator("page_url")
    def validate_page_url(cls, v: str) -> str:
        """Ensure page URL is from our domain."""
        # Allow our domains and localhost
        allowed_prefixes = ("http://localhost", "https://soban-saleem.github.io")
        if not v.startswith(allowed_prefixes):
            raise ValueError("Invalid page URL")
        return v


# =============================================================================
# Session Management
# =============================================================================


def generate_cache_key(question: str, selected_text: str | None = None) -> str:
    """
    Generate a cache key for a request.

    Args:
        question: User's question
        selected_text: Optional selected text

    Returns:
        str: SHA-256 hash for cache key
    """
    content = question.lower().strip()
    if selected_text:
        content += f"|{selected_text.lower().strip()}"
    return hashlib.sha256(content.encode()).hexdigest()


# =============================================================================
# Type Aliases
# =============================================================================

SessionIdDep = Annotated[str, check_rate_limit]
"""Dependency that provides session ID and enforces rate limiting."""
