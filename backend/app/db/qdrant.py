"""
Qdrant vector database client and connection management.
Handles vector storage for textbook content chunks.
"""

import logging
from typing import Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
)
from qdrant_client.http.exceptions import UnexpectedResponse

from app.core.config import get_settings
from app.core.exceptions import ServiceUnavailableException

logger = logging.getLogger(__name__)

# Collection name for storing textbook content chunks
TEXTBOOK_CHUNKS_COLLECTION = "textbook_chunks"

# Vector configuration
EMBEDDING_DIMENSIONS = 1536  # OpenAI text-embedding-3-small output dimensions
VECTOR_DISTANCE = Distance.COSINE


class QdrantService:
    """
    Qdrant vector database service.

    Manages connection to Qdrant and provides methods for
    storing and searching content embeddings.
    """

    def __init__(self) -> None:
        """Initialize the Qdrant service with configuration."""
        self.settings = get_settings()
        self._client: Optional[QdrantClient] = None
        self._initialized = False

    @property
    def client(self) -> QdrantClient:
        """
        Get or create the Qdrant client.

        Returns:
            QdrantClient: Active Qdrant client instance

        Raises:
            ServiceUnavailableException: If connection fails
        """
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> QdrantClient:
        """
        Create a new Qdrant client instance.

        Returns:
            QdrantClient: Configured client

        Raises:
            ServiceUnavailableException: If client creation fails
        """
        try:
            client = QdrantClient(
                url=self.settings.QDRANT_URL,
                api_key=self.settings.QDRANT_API_KEY or None,
                timeout=30,
            )
            # Verify connection
            client.get_collections()
            logger.info(f"Connected to Qdrant at {self.settings.QDRANT_URL}")
            return client
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise ServiceUnavailableException(
                message="Vector database service unavailable",
                service="qdrant",
                retry_after=30,
                details={"error": str(e)},
            ) from e

    async def initialize_collection(self) -> bool:
        """
        Initialize the textbook chunks collection.

        Creates the collection if it doesn't exist.
        Verifies collection schema if it does exist.

        Returns:
            bool: True if collection is ready for use

        Raises:
            ServiceUnavailableException: If initialization fails
        """
        try:
            collections = self.client.get_collections()
            existing_collections = [c.name for c in collections.collections]

            if TEXTBOOK_CHUNKS_COLLECTION in existing_collections:
                # Verify collection configuration matches expectations
                collection_info = self.client.get_collection(TEXTBOOK_CHUNKS_COLLECTION)
                expected_dim = collection_info.config.params.vectors.size
                if expected_dim != EMBEDDING_DIMENSIONS:
                    raise ValueError(
                        f"Collection '{TEXTBOOK_CHUNKS_COLLECTION}' has {expected_dim} dimensions, "
                        f"expected {EMBEDDING_DIMENSIONS}"
                    )
                logger.info(f"Collection '{TEXTBOOK_CHUNKS_COLLECTION}' already exists and is valid")
            else:
                # Create new collection
                self.client.create_collection(
                    collection_name=TEXTBOOK_CHUNKS_COLLECTION,
                    vectors_config=VectorParams(
                        size=EMBEDDING_DIMENSIONS,
                        distance=VECTOR_DISTANCE,
                    ),
                )
                logger.info(f"Created collection '{TEXTBOOK_CHUNKS_COLLECTION}'")

            self._initialized = True
            return True

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during collection initialization: {e}")
            raise ServiceUnavailableException(
                message="Failed to initialize vector collection",
                service="qdrant",
                details={"error": str(e)},
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error during collection initialization: {e}")
            raise ServiceUnavailableException(
                message="Failed to initialize vector collection",
                service="qdrant",
                details={"error": str(e)},
            ) from e

    async def upsert_chunks(
        self,
        chunks: list[dict[str, Any]],
    ) -> None:
        """
        Insert or update content chunks in the collection.

        Args:
            chunks: List of chunks with id, vector, and payload

        Raises:
            ServiceUnavailableException: If upsert fails
        """
        try:
            points = [
                PointStruct(
                    id=chunk["chunk_id"],
                    vector=chunk["embedding"],
                    payload=chunk["payload"],
                )
                for chunk in chunks
            ]

            self.client.upsert(
                collection_name=TEXTBOOK_CHUNKS_COLLECTION,
                points=points,
            )
            logger.info(f"Upserted {len(points)} chunks to Qdrant")

        except Exception as e:
            logger.error(f"Failed to upsert chunks: {e}")
            raise ServiceUnavailableException(
                message="Failed to store content chunks",
                service="qdrant",
                details={"error": str(e)},
            ) from e

    async def search_chunks(
        self,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: float = 0.5,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for similar content chunks.

        Args:
            query_vector: Embedding vector for the query
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0-1)
            filters: Optional metadata filters

        Returns:
            List of matching chunks with scores and payloads

        Raises:
            ServiceUnavailableException: If search fails
        """
        try:
            search_filter = None
            if filters:
                conditions = [
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value),
                    )
                    for key, value in filters.items()
                ]
                search_filter = Filter(must=conditions)

            results = self.client.search(
                collection_name=TEXTBOOK_CHUNKS_COLLECTION,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=search_filter,
            )

            chunks = [
                {
                    "chunk_id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                }
                for result in results
            ]

            logger.debug(f"Found {len(chunks)} chunks for query")
            return chunks

        except Exception as e:
            logger.error(f"Failed to search chunks: {e}")
            raise ServiceUnavailableException(
                message="Failed to search content",
                service="qdrant",
                details={"error": str(e)},
            ) from e

    async def delete_collection(self) -> bool:
        """
        Delete the textbook chunks collection.

        Use with caution! This will remove all indexed content.

        Returns:
            bool: True if collection was deleted

        Raises:
            ServiceUnavailableException: If deletion fails
        """
        try:
            self.client.delete_collection(TEXTBOOK_CHUNKS_COLLECTION)
            logger.warning(f"Deleted collection '{TEXTBOOK_CHUNKS_COLLECTION}'")
            self._initialized = False
            return True

        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise ServiceUnavailableException(
                message="Failed to delete collection",
                service="qdrant",
                details={"error": str(e)},
            ) from e

    async def collection_info(self) -> dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection stats

        Raises:
            ServiceUnavailableException: If info retrieval fails
        """
        try:
            info = self.client.get_collection(TEXTBOOK_CHUNKS_COLLECTION)
            return {
                "name": TEXTBOOK_CHUNKS_COLLECTION,
                "vectors_count": info.points_count,
                "indexed_vectors_count": info.indexed_vectors_count,
                "dimensions": info.config.params.vectors.size,
                "distance": str(info.config.params.vectors.distance),
            }

        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise ServiceUnavailableException(
                message="Failed to get collection info",
                service="qdrant",
                details={"error": str(e)},
            ) from e

    def is_initialized(self) -> bool:
        """Check if the collection has been initialized."""
        return self._initialized

    async def close(self) -> None:
        """Close the Qdrant client connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._initialized = False
            logger.info("Qdrant client closed")


# Global service instance
_qdrant_service: Optional[QdrantService] = None


def get_qdrant_service() -> QdrantService:
    """
    Get the singleton Qdrant service instance.

    Returns:
        QdrantService: Active Qdrant service
    """
    global _qdrant_service
    if _qdrant_service is None:
        _qdrant_service = QdrantService()
    return _qdrant_service
