"""
Vector retrieval service using Qdrant.

Handles searching for relevant content chunks based on
semantic similarity to user queries.
"""

import logging
from typing import Any, List, Optional

from app.db.qdrant import get_qdrant_service
from app.models.chat import CitationReference
from app.models.document import SearchResult
from app.services.embedding import get_embedding_service
from app.core.exceptions import NoResultsFoundException

logger = logging.getLogger(__name__)


class RetrievalService:
    """
    Service for retrieving relevant content from Qdrant.

    Takes a user question, generates an embedding, and searches
    for the most semantically similar content chunks.
    """

    def __init__(self) -> None:
        """Initialize the retrieval service."""
        self.qdrant = get_qdrant_service()
        self.embedding_service = get_embedding_service()

    async def search(
        self,
        question: str,
        limit: int = 5,
        score_threshold: float = 0.5,
        filters: dict[str, Any] | None = None,
    ) -> List[SearchResult]:
        """
        Search for relevant content chunks based on a question.

        Args:
            question: User's question
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0-1)
            filters: Optional metadata filters (e.g., module_id)

        Returns:
            List of search results with scores and metadata

        Raises:
            NoResultsFoundException: If no relevant chunks found
            ServiceUnavailableException: If search fails
        """
        # Generate embedding for the question
        embedding = await self.embedding_service.generate_embedding(question)

        # Search Qdrant
        chunks = await self.qdrant.search_chunks(
            query_vector=embedding,
            limit=limit,
            score_threshold=score_threshold,
            filters=filters,
        )

        if not chunks:
            raise NoResultsFoundException(
                message="No relevant content found in the textbook",
                suggested_topics=self._get_suggested_topics(filters),
            )

        # Convert to SearchResult objects
        results = []
        for chunk in chunks:
            payload = chunk["payload"]
            results.append(
                SearchResult(
                    chunk_id=str(chunk["chunk_id"]),
                    score=chunk["score"],
                    text=payload["text"],
                    metadata={
                        "module_id": payload["module_id"],
                        "lesson_title": payload["lesson_title"],
                        "section_heading": payload.get("section_heading"),
                        "url_anchor": payload["url_anchor"],
                        "chunk_index": payload["chunk_index"],
                        "token_count": payload["token_count"],
                    },
                )
            )

        logger.info(f"Found {len(results)} chunks for question")
        return results

    async def search_with_selection_bias(
        self,
        question: str,
        selected_text: str,
        page_url: str,
        limit: int = 5,
    ) -> List[SearchResult]:
        """
        Search with bias toward content from the selected page.

        Used for text-selection mode where we want to prioritize
        chunks from the same page as the selected text.

        Args:
            question: User's question
            selected_text: Text selected by the user
            page_url: URL of the page with selection
            limit: Maximum results

        Returns:
            List of biased search results
        """
        # Extract module/lesson from page URL for filtering
        module_id = self._extract_module_from_url(page_url)

        # First, try to get chunks from the same module
        if module_id:
            try:
                module_chunks = await self.search(
                    question=f"{question} (context: {selected_text[:200]})",
                    limit=limit,
                    score_threshold=0.3,  # Lower threshold for selection mode
                    filters={"module_id": module_id} if module_id else None,
                )

                if module_chunks:
                    logger.info(f"Found {len(module_chunks)} chunks from same module")
                    return module_chunks
            except NoResultsFoundException:
                logger.info("No chunks from same module, falling back to global search")

        # Fallback to global search
        return await self.search(
            question=question,
            limit=limit,
            score_threshold=0.4,
        )

    def _extract_module_from_url(self, url: str) -> Optional[str]:
        """
        Extract module ID from a page URL.

        Args:
            url: Page URL

        Returns:
            Module ID if found, None otherwise
        """
        # Expected format: /module1-sensors/...
        parts = url.strip("/").split("/")
        if parts and parts[0].startswith("module"):
            return parts[0]
        return None

    def _get_suggested_topics(
        self,
        filters: dict[str, Any] | None,
    ) -> List[str]:
        """
        Get suggested topics when no results are found.

        Args:
            filters: Active search filters

        Returns:
            List of suggested topics to explore
        """
        # Common topics in the textbook
        common_topics = [
            "ROS 2 fundamentals",
            "sensors (LIDAR, IMU, cameras)",
            "robot simulation with Gazebo",
            "NVIDIA Isaac platform",
            "kinematics and motion planning",
            "humanoid robot control",
        ]

        if filters and "module_id" in filters:
            # Suggest related topics based on module
            module = filters["module_id"]
            if "ros2" in module:
                return ["ROS 2 nodes", "ROS 2 topics", "ROS 2 services"]
            elif "sensor" in module:
                return ["LIDAR", "IMU", "computer vision"]
            elif "isaac" in module:
                return ["Isaac Sim", "Isaac ROS", "navigation"]

        return common_topics[:3]

    async def get_retrieval_stats(self) -> dict[str, Any]:
        """
        Get statistics about the vector collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            info = await self.qdrant.collection_info()
            return {
                "total_chunks": info.get("vectors_count", 0),
                "dimensions": info.get("dimensions", 0),
                "distance_metric": info.get("distance", "unknown"),
                "collection_ready": self.qdrant.is_initialized(),
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {
                "error": str(e),
                "collection_ready": False,
            }


# Global service instance
_retrieval_service: RetrievalService | None = None


def get_retrieval_service() -> RetrievalService:
    """
    Get the singleton retrieval service instance.

    Returns:
        RetrievalService: Active retrieval service
    """
    global _retrieval_service
    if _retrieval_service is None:
        _retrieval_service = RetrievalService()
    return _retrieval_service
