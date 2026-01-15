"""
OpenAI embedding service.

Generates vector embeddings for text using OpenAI's text-embedding-3-small model.
"""

import logging
from typing import List

import tiktoken
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

from app.core.config import get_settings
from app.core.exceptions import ServiceUnavailableException, RateLimitException

logger = logging.getLogger(__name__)

settings = get_settings()


class EmbeddingService:
    """
    Service for generating text embeddings using OpenAI.

    Uses text-embedding-3-small which outputs 1536-dimensional vectors.
    """

    def __init__(self) -> None:
        """Initialize the embedding service."""
        self.settings = get_settings()
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        """Get or create the OpenAI client."""
        if self._client is None:
            self._client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        return self._client

    async def generate_embedding(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate an embedding vector for the given text.

        Args:
            text: Text to embed

        Returns:
            List of 1536 float values representing the embedding

        Raises:
            ServiceUnavailableException: If OpenAI API is unavailable
            RateLimitException: If rate limit is exceeded
        """
        try:
            response = self.client.embeddings.create(
                model=self.settings.OPENAI_EMBEDDING_MODEL,
                input=text[:8191],  # OpenAI limit
            )

            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")
            return embedding

        except RateLimitException as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise RateLimitException(
                message="Embedding rate limit exceeded",
                retry_after=60,
                details={"error": str(e)},
            ) from e

        except (APIConnectionError, APIError) as e:
            logger.error(f"OpenAI API error: {e}")
            raise ServiceUnavailableException(
                message="Failed to generate embedding",
                service="openai",
                retry_after=30,
                details={"error": str(e)},
            ) from e

    async def generate_embeddings_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in a single API call.

        Args:
            texts: List of texts to embed (max 2048 texts per call)

        Returns:
            List of embedding vectors

        Raises:
            ServiceUnavailableException: If OpenAI API fails
            RateLimitException: If rate limit is exceeded
        """
        if not texts:
            return []

        try:
            # Truncate texts to max length
            truncated_texts = [text[:8191] for text in texts]

            response = self.client.embeddings.create(
                model=self.settings.OPENAI_EMBEDDING_MODEL,
                input=truncated_texts,
            )

            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} embeddings in batch")
            return embeddings

        except RateLimitException as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise RateLimitException(
                message="Embedding rate limit exceeded",
                retry_after=60,
            ) from e

        except (APIConnectionError, APIError) as e:
            logger.error(f"OpenAI API error: {e}")
            raise ServiceUnavailableException(
                message="Failed to generate embeddings",
                service="openai",
                retry_after=30,
            ) from e

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in text using tiktoken.

        Args:
            text: Text to count tokens in

        Returns:
            int: Number of tokens
        """
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception as e:
            logger.error(f"Failed to count tokens: {e}")
            # Fallback to approximate count (1 token ≈ 4 chars)
            return len(text) // 4


# Global service instance
_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    """
    Get the singleton embedding service instance.

    Returns:
        EmbeddingService: Active embedding service
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
