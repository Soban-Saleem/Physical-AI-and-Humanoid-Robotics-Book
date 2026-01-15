"""
Custom exceptions for the RAG chatbot application.
Provides specific exception types for different error scenarios.
"""

from typing import Any


class ChatbotException(Exception):
    """Base exception for all chatbot-related errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        """
        Initialize the exception.

        Args:
            message: Human-readable error message
            details: Additional error details for logging/debugging
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ServiceUnavailableException(ChatbotException):
    """
    Raised when an external service (OpenAI, Qdrant) is unavailable.

    Includes retry_after hint for client-side retry logic.
    """

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        service: str = "unknown",
        retry_after: int = 30,
        details: dict[str, Any] | None = None,
    ):
        """
        Initialize service unavailable exception.

        Args:
            message: Human-readable error message
            service: Name of the unavailable service (openai, qdrant, neon)
            retry_after: Seconds before retry is recommended
            details: Additional error details
        """
        self.service = service
        self.retry_after = retry_after
        full_details = {"service": service, "retry_after": retry_after}
        if details:
            full_details.update(details)
        super().__init__(message, full_details)


class RateLimitException(ChatbotException):
    """
    Raised when the request rate exceeds allowed limits.

    Includes retry_after hint for client-side retry logic.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int = 60,
        details: dict[str, Any] | None = None,
    ):
        """
        Initialize rate limit exception.

        Args:
            message: Human-readable error message
            retry_after: Seconds before retry is recommended
            details: Additional error details
        """
        self.retry_after = retry_after
        full_details = {"retry_after": retry_after}
        if details:
            full_details.update(details)
        super().__init__(message, full_details)


class NoResultsFoundException(ChatbotException):
    """
    Raised when no relevant content is found in the textbook.

    This is expected behavior for questions outside the course material.
    """

    def __init__(
        self,
        message: str = "No relevant content found in the textbook",
        suggested_topics: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ):
        """
        Initialize no results exception.

        Args:
            message: Human-readable error message
            suggested_topics: Topics the user might want to explore
            details: Additional error details
        """
        self.suggested_topics = suggested_topics or []
        full_details = {"suggested_topics": self.suggested_topics}
        if details:
            full_details.update(details)
        super().__init__(message, full_details)


class ValidationException(ChatbotException):
    """
    Raised when request validation fails.
    """

    def __init__(
        self,
        message: str,
        field: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        """
        Initialize validation exception.

        Args:
            message: Human-readable error message
            field: Name of the field that failed validation
            details: Additional error details
        """
        self.field = field
        full_details = {"field": field} if field else {}
        if details:
            full_details.update(details)
        super().__init__(message, full_details)


class ContentIndexingException(ChatbotException):
    """
    Raised during content indexing pipeline failures.
    """

    def __init__(
        self,
        message: str,
        file_path: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        """
        Initialize content indexing exception.

        Args:
            message: Human-readable error message
            file_path: Path to the file that caused the error
            details: Additional error details
        """
        self.file_path = file_path
        full_details = {"file_path": file_path} if file_path else {}
        if details:
            full_details.update(details)
        super().__init__(message, full_details)
