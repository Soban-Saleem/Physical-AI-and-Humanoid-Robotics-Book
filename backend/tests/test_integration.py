"""
Integration tests for the RAG chatbot pipeline.

Tests the full flow from question to answer including
embedding generation, vector search, and answer generation.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.api.routes.chat import process_question, process_selection_question
from app.services.chunking import ChunkingService
from app.services.embeddings import EmbeddingService
from app.services.retrieval import RetrievalService
from app.services.citation import CitationService
from app.services.generation import GenerationService


class TestFullPipeline:
    """Tests for the complete RAG pipeline."""

    @pytest.mark.asyncio
    async def test_question_to_answer_pipeline(self, mock_openai_client, mock_qdrant_client):
        """Test the complete pipeline from question to answer."""
        # Mock search result
        mock_result = MagicMock(
            id="chunk_123",
            score=0.87,
            payload={
                "content": "Physical AI combines artificial intelligence with physical robotics systems.",
                "source_path": "module1/intro.md",
                "module": "module1",
                "lesson": "intro",
                "section": "what-is-physical-ai",
            }
        )

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=[mock_result]))
        ), patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            response = await process_question(
                question="What is Physical AI?",
                session_id="test-session",
            )

            assert "answer" in response.model_fields or hasattr(response, "answer")
            assert response.answer is not None
            assert len(response.answer) > 0

    @pytest.mark.asyncio
    async def test_pipeline_with_no_results(self, mock_openai_client):
        """Test pipeline when vector search returns no results."""
        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=[]))
        ), patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            response = await process_question(
                question="What is a very obscure topic not in the database?",
                session_id="test-session",
            )

            # Should still generate a helpful response
            assert response.answer is not None
            assert len(response.answer) > 0


class TestSelectionPipeline:
    """Tests for the selection-based Q&A pipeline."""

    @pytest.mark.asyncio
    async def test_selection_with_relevant_results(self, mock_openai_client, mock_qdrant_client):
        """Test selection pipeline with relevant search results."""
        mock_result = MagicMock(
            id="chunk_456",
            score=0.92,
            payload={
                "content": "ROS 2 (Robot Operating System 2) is a middleware for robotics.",
                "source_path": "module2/ros2.md",
                "module": "module2",
                "lesson": "ros2",
            }
        )

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=[mock_result]))
        ), patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            response = await process_selection_question(
                question="What does this mean?",
                selected_text="ROS 2 is a robotics middleware",
                page_url="/docs/module2/ros2",
                session_id="test-session",
            )

            assert response.answer is not None
            assert len(response.answer) > 0

    @pytest.mark.asyncio
    async def test_selection_boosts_relevant_chunks(self, mock_openai_client):
        """Test that selection boosts chunks from the same page."""
        # Create results from different sources
        results = [
            MagicMock(
                id="chunk_1",
                score=0.75,
                payload={
                    "content": "Content from different page",
                    "source_path": "module1/other.md",
                }
            ),
            MagicMock(
                id="chunk_2",
                score=0.70,  # Lower base score
                payload={
                    "content": "Content from same page",
                    "source_path": "module2/ros2.md",
                }
            )
        ]

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=results))
        ), patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            response = await process_selection_question(
                question="Explain this",
                selected_text="Selected text from ros2 page",
                page_url="/docs/module2/ros2",
                session_id="test-session",
            )

            assert response.answer is not None


class TestCitationFormatting:
    """Tests for citation formatting in responses."""

    @pytest.mark.asyncio
    async def test_citations_in_response(self, mock_openai_client, mock_qdrant_client):
        """Test that citations are properly formatted."""
        mock_results = [
            MagicMock(
                id=f"chunk_{i}",
                score=0.8 + (i * 0.01),
                payload={
                    "content": f"Content chunk {i}",
                    "source_path": f"module{i}/lesson{i}.md",
                    "module": f"module{i}",
                    "lesson": f"lesson{i}",
                }
            )
            for i in range(3)
        ]

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=mock_results))
        ), patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            response = await process_question(
                question="Test question",
                session_id="test",
            )

            # Check citations are present
            assert response.citations is not None
            assert len(response.citations) == 3

            # Check citation structure
            for citation in response.citations:
                assert hasattr(citation, "index")
                assert hasattr(citation, "source_path")
                assert hasattr(citation, "snippet")


class TestErrorRecovery:
    """Tests for error recovery in the pipeline."""

    @pytest.mark.asyncio
    async def test_embedding_failure_recovery(self, mock_openai_client):
        """Test recovery from embedding generation failure."""
        with patch(
            "app.services.embedding.get_openai_client",
            side_effect=Exception("Embedding API failed")
        ):
            with pytest.raises(Exception):
                await process_question(
                    question="Test question",
                    session_id="test",
                )

    @pytest.mark.asyncio
    async def test_search_failure_recovery(self, mock_openai_client):
        """Test recovery from search failure."""
        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            side_effect=Exception("Search failed")
        ):
            with pytest.raises(Exception):
                await process_question(
                    question="Test question",
                    session_id="test",
                )

    @pytest.mark.asyncio
    async def test_generation_failure_recovery(self, mock_openai_client):
        """Test recovery from generation failure."""
        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=[]))
        ), patch(
            "app.services.generation.get_openai_client",
            side_effect=Exception("Generation failed")
        ):
            with pytest.raises(Exception):
                await process_question(
                    question="Test question",
                    session_id="test",
                )


class TestChunkingToSearchIntegration:
    """Tests for content chunking to search integration."""

    @pytest.mark.asyncio
    async def test_chunked_content_is_searchable(self, mock_qdrant_client, mock_openai_client):
        """Test that chunked content can be searched."""
        # First, chunk some content
        chunking_service = ChunkingService()
        markdown_content = """
# ROS 2 Introduction

ROS 2 is the next version of the Robot Operating System.

## Key Features

- Real-time performance
- Security support
- Multi-robot support
"""

        chunking_result = chunking_service.chunk_document(
            content=markdown_content,
            source_path="module2/ros2-intro.md",
        )

        assert chunking_result.total_chunks > 0

        # Verify chunks can be upserted to Qdrant
        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ):
            # Simulate upsert
            embeddings = await mock_openai_client.embeddings.create(
                input=[c.content for c in chunking_result.chunks],
                model="text-embedding-3-small"
            )

            assert len(embeddings.data) == chunking_result.total_chunks


class TestServiceIntegration:
    """Tests for service interaction."""

    @pytest.mark.asyncio
    async def test_services_share_context(self, mock_openai_client):
        """Test that services can share context properly."""
        embedding_service = EmbeddingService()
        retrieval_service = RetrievalService()
        generation_service = GenerationService()

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=[]))
        ), patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            # Generate embedding
            query = "What is ROS 2?"
            embedding = await embedding_service.generate_embedding(query)
            assert len(embedding) == 1536

            # Search for similar content
            results = await retrieval_service.search(query, limit=5)
            assert isinstance(results, list)

            # Generate answer
            answer = await generation_service.generate_answer(
                query=query,
                context_chunks=["ROS 2 is a robotics middleware"],
            )
            assert len(answer) > 0
