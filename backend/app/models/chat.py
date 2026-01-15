"""
Pydantic models for chat API requests and responses.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


# =============================================================================
# Citation References
# =============================================================================


class CitationReference(BaseModel):
    """
    Reference to source material for a chatbot response.

    Links a response to the specific location in the textbook
    where the information was found.
    """

    citationId: str = Field(
        ...,
        description="Unique identifier for this citation",
    )
    moduleId: str = Field(
        ...,
        description="Module identifier (e.g., 'module1-ros2')",
    )
    lessonTitle: str = Field(
        ...,
        description="Title of the lesson",
    )
    sectionHeading: Optional[str] = Field(
        None,
        description="Section heading within the lesson",
    )
    urlAnchor: str = Field(
        ...,
        description="URL anchor to jump to the source",
    )
    relevanceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Similarity score (0-1)",
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "citationId": "cite_001",
                "moduleId": "module1-sensors",
                "lessonTitle": "Introduction to Sensors",
                "sectionHeading": "LIDAR",
                "urlAnchor": "/module1-sensors/introduction#lidar",
                "relevanceScore": 0.92,
            }
        }


# =============================================================================
# Chat Messages
# =============================================================================


class ChatMessage(BaseModel):
    """
    A single message in a conversation.

    Represents either a user question or an assistant response.
    """

    messageId: str = Field(..., description="Unique message identifier")
    messageType: str = Field(
        ...,
        pattern="^(user|assistant)$",
        description="Message type: 'user' or 'assistant'",
    )
    content: str = Field(..., description="Message content")
    citations: Optional[List[CitationReference]] = Field(
        None,
        description="Citations for assistant responses",
    )
    createdAt: int = Field(..., description="Unix timestamp in milliseconds")
    isCached: Optional[bool] = Field(
        None,
        description="Whether this was a cached response",
    )


# =============================================================================
# Request Models
# =============================================================================


class ChatRequest(BaseModel):
    """
    Request payload for the /chat endpoint.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's question about the textbook content",
    )
    contextMessages: Optional[List[ChatMessage]] = Field(
        None,
        description="Conversation history for context",
    )
    sessionId: Optional[str] = Field(
        None,
        description="Session identifier for conversation continuity",
    )

    @field_validator("question")
    def question_not_empty(cls, v: str) -> str:
        """Ensure question is not just whitespace."""
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "question": "What is the difference between LIDAR and IMU?",
                "contextMessages": None,
                "sessionId": "session_abc123",
            }
        }


class ChatSelectionRequest(BaseModel):
    """
    Request payload for the /chat/selection endpoint.

    Used when the user has selected specific text and wants
    the chatbot to answer based only on that selection.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's question about the selected text",
    )
    selectedText: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Text selected by the user on the page",
    )
    pageUrl: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="URL of the page where text was selected",
    )
    contextMessages: Optional[List[ChatMessage]] = Field(
        None,
        description="Conversation history for context",
    )
    sessionId: Optional[str] = Field(
        None,
        description="Session identifier for conversation continuity",
    )

    @field_validator("question")
    def question_not_empty(cls, v: str) -> str:
        """Ensure question is not just whitespace."""
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()

    @field_validator("selectedText")
    def selection_not_empty(cls, v: str) -> str:
        """Ensure selection is not just whitespace."""
        if not v.strip():
            raise ValueError("Selected text cannot be empty")
        return v.strip()

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "question": "Explain this",
                "selectedText": "LIDAR (Light Detection and Ranging) is a...",
                "pageUrl": "https://example.com/module1/sensors",
                "contextMessages": None,
                "sessionId": "session_abc123",
            }
        }


# =============================================================================
# Response Models
# =============================================================================


class ChatResponse(BaseModel):
    """
    Response payload for chat endpoints.
    """

    answer: str = Field(
        ...,
        description="Chatbot's answer to the question",
    )
    citations: List[CitationReference] = Field(
        ...,
        description="Source citations for the answer",
    )
    sessionId: str = Field(
        ...,
        description="Session identifier",
    )
    isCached: bool = Field(
        False,
        description="Whether this response was from cache",
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "answer": "LIDAR uses laser pulses to measure distances...",
                "citations": [
                    {
                        "citationId": "cite_001",
                        "moduleId": "module1-sensors",
                        "lessonTitle": "Introduction to Sensors",
                        "sectionHeading": "LIDAR",
                        "urlAnchor": "/module1/sensors#lidar",
                        "relevanceScore": 0.92,
                    }
                ],
                "sessionId": "session_abc123",
                "isCached": False,
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response format.
    """

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    retryAfter: Optional[int] = Field(
        None,
        description="Seconds before retry (for rate limits and service unavailability)",
    )


# =============================================================================
# Health Check Models
# =============================================================================


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str = Field(
        ...,
        pattern="^(healthy|degraded|unhealthy)$",
        description="Overall service status",
    )
    services: dict[str, bool] = Field(
        ...,
        description="Status of individual services",
    )
    timestamp: int = Field(..., description="Unix timestamp in milliseconds")
