"""
Pydantic models for document/content chunk processing.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# =============================================================================
# Content Chunk Models
# =============================================================================


class ChunkMetadata(BaseModel):
    """
    Metadata for a content chunk.

    Contains information about where in the textbook
    the chunk originated.
    """

    module_id: str = Field(
        ...,
        description="Module identifier (e.g., 'module1-ros2')",
    )
    lesson_title: str = Field(
        ...,
        description="Title of the lesson",
    )
    section_heading: Optional[str] = Field(
        None,
        description="Section heading within the lesson",
    )
    url_anchor: str = Field(
        ...,
        description="URL anchor linking to the source",
    )
    chunk_index: int = Field(
        ...,
        ge=0,
        description="Sequential index of this chunk within the section",
    )
    token_count: int = Field(
        ...,
        ge=0,
        description="Number of tokens in this chunk",
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "module_id": "module1-sensors",
                "lesson_title": "Introduction to Sensors",
                "section_heading": "LIDAR",
                "url_anchor": "/module1/sensors#lidar",
                "chunk_index": 0,
                "token_count": 342,
            }
        }


class ContentChunk(BaseModel):
    """
    A semantically meaningful portion of textbook content.

    Created by markdown-aware chunking that preserves
    paragraph structure and keeps code blocks intact.
    """

    chunk_id: str = Field(..., description="Unique chunk identifier")
    text: str = Field(..., description="Chunk text content")
    metadata: ChunkMetadata = Field(..., description="Source metadata")
    embedding: Optional[List[float]] = Field(
        None,
        description="Vector embedding (1536 dimensions for text-embedding-3-small)",
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "chunk_id": "chunk_001",
                "text": "LIDAR (Light Detection and Ranging) is a remote sensing method...",
                "metadata": {
                    "module_id": "module1-sensors",
                    "lesson_title": "Introduction to Sensors",
                    "section_heading": "LIDAR",
                    "url_anchor": "/module1/sensors#lidar",
                    "chunk_index": 0,
                    "token_count": 342,
                },
                "embedding": None,  # Added during indexing
            }
        }


# =============================================================================
# Indexing Models
# =============================================================================


class IndexingRequest(BaseModel):
    """
    Request to index content from the textbook.
    """

    module_filter: Optional[str] = Field(
        None,
        description="Only index specific module (if specified)",
    )
    force_reindex: bool = Field(
        False,
        description="Re-index even if content already indexed",
    )


class IndexingResult(BaseModel):
    """
    Result of a content indexing operation.
    """

    total_chunks: int = Field(..., description="Total chunks indexed")
    modules_processed: List[str] = Field(..., description="Modules that were indexed")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    duration_seconds: float = Field(..., description="Time taken for indexing")
    timestamp: int = Field(..., description="Unix timestamp when indexing completed")


# =============================================================================
# Qdrant Payload Models
# =============================================================================


class QdrantPayload(BaseModel):
    """
    Payload structure for Qdrant points.

    Matches the ChunkMetadata structure for easy reconstruction.
    """

    text: str = Field(..., description="Chunk text content")
    module_id: str = Field(..., description="Module identifier")
    lesson_title: str = Field(..., description="Lesson title")
    section_heading: Optional[str] = Field(None, description="Section heading")
    url_anchor: str = Field(..., description="URL to source")
    chunk_index: int = Field(..., description="Chunk index")
    token_count: int = Field(..., description="Token count")

    @classmethod
    def from_content_chunk(cls, chunk: ContentChunk) -> "QdrantPayload":
        """Create QdrantPayload from ContentChunk."""
        return cls(
            text=chunk.text,
            module_id=chunk.metadata.module_id,
            lesson_title=chunk.metadata.lesson_title,
            section_heading=chunk.metadata.section_heading,
            url_anchor=chunk.metadata.url_anchor,
            chunk_index=chunk.metadata.chunk_index,
            token_count=chunk.metadata.token_count,
        )

    def to_citation_reference(
        self,
        citation_id: str,
        relevance_score: float,
    ) -> "CitationReference":
        """Convert to CitationReference."""
        from app.models.chat import CitationReference

        return CitationReference(
            citationId=citation_id,
            moduleId=self.module_id,
            lessonTitle=self.lesson_title,
            sectionHeading=self.section_heading,
            urlAnchor=self.url_anchor,
            relevanceScore=relevance_score,
        )


# =============================================================================
# Search Result Models
# =============================================================================


class SearchResult(BaseModel):
    """
    A search result from Qdrant.

    Includes the chunk content, relevance score, and metadata.
    """

    chunk_id: str = Field(..., description="Unique chunk identifier")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    text: str = Field(..., description="Chunk text content")
    metadata: ChunkMetadata = Field(..., description="Source metadata")
