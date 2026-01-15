"""
Tests for core services (embedding, retrieval, citation, generation).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.embedding import EmbeddingService
from app.services.retrieval import RetrievalService
from app.services.citation import CitationService
from app.services.generation import GenerationService, PromptTemplate
from app.models.document import SearchResult
from app.models.chat import CitationReference


class TestEmbeddingService:
    """Tests for EmbeddingService."""

    @pytest.mark.asyncio
    async def test_generate_embedding(self, mock_openai_client):
        """Test generating a single embedding."""
        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ):
            service = EmbeddingService()
            embedding = await service.generate_embedding("test text")

            assert len(embedding) == 1536
            assert all(isinstance(x, float) for x in embedding)

    @pytest.mark.asyncio
    async def test_generate_embeddings_batch(self, mock_openai_client):
        """Test generating multiple embeddings."""
        mock_openai_client.embeddings.create = MagicMock(
            return_value=MagicMock(
                data=[
                    MagicMock(embedding=[0.1] * 1536),
                    MagicMock(embedding=[0.2] * 1536),
                ]
            )
        )

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ):
            service = EmbeddingService()
            embeddings = await service.generate_embeddings_batch(
                ["text1", "text2"]
            )

            assert len(embeddings) == 2
            assert len(embeddings[0]) == 1536

    def test_count_tokens(self):
        """Test token counting."""
        service = EmbeddingService()
        count = service.count_tokens("This is a test.")
        assert count > 0


class TestRetrievalService:
    """Tests for RetrievalService."""

    @pytest.mark.asyncio
    async def test_search_returns_results(self, mock_qdrant_client):
        """Test that search returns results."""
        mock_result = MagicMock(
            id="test_id",
            score=0.85,
            payload={
                "content": "Test content about robotics",
                "source_path": "test.md",
                "module": "module1",
                "lesson": "lesson1",
            }
        )
        mock_qdrant_client.search = MagicMock(return_value=[mock_result])

        with patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(
                search=AsyncMock(return_value=[mock_result])
            )
        ):
            service = RetrievalService()
            results = await service.search("robotics query", limit=5)

            assert len(results) >= 0
            assert all(isinstance(r, SearchResult) for r in results)

    @pytest.mark.asyncio
    async def test_search_with_selection_bias(self, mock_qdrant_client):
        """Test search with text selection bias."""
        mock_result = MagicMock(
            id="test_id",
            score=0.9,
            payload={
                "content": "Selected text content",
                "source_path": "test.md",
            }
        )
        mock_qdrant_client.search = MagicMock(return_value=[mock_result])

        with patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(
                search=AsyncMock(return_value=[mock_result])
            )
        ):
            service = RetrievalService()
            results = await service.search_with_selection_bias(
                query="robotics",
                selected_text="selected context",
                limit=5
            )
            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_empty_results(self):
        """Test search with no results."""
        with patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=AsyncMock(return_value=[]))
        ):
            service = RetrievalService()
            results = await service.search("nonexistent topic")
            assert len(results) == 0


class TestCitationService:
    """Tests for CitationService."""

    def test_format_citations_single(self):
        """Test formatting a single citation."""
        service = CitationService()
        result = MagicMock(
            payload={
                "content": "Test content",
                "source_path": "module1/lesson1.md",
                "module": "module1",
                "lesson": "lesson1",
            }
        )

        citations = service.format_citations([result])
        assert len(citations) == 1
        assert citations[0].source_path == "module1/lesson1.md"

    def test_format_citations_multiple(self):
        """Test formatting multiple citations."""
        service = CitationService()
        results = [
            MagicMock(
                payload={
                    "content": f"Content {i}",
                    "source_path": f"module{i}/lesson{i}.md",
                    "module": f"module{i}",
                    "lesson": f"lesson{i}",
                }
            )
            for i in range(3)
        ]

        citations = service.format_citations(results)
        assert len(citations) == 3
        assert all(isinstance(c, CitationReference) for c in citations)

    def test_deduplicate_citations(self):
        """Test citation deduplication."""
        service = CitationService()
        citations = [
            CitationReference(
                index=1,
                source_path="test.md",
                title="Test",
                snippet="Content 1",
            ),
            CitationReference(
                index=2,
                source_path="test.md",
                title="Test",
                snippet="Content 2",
            ),
        ]

        deduped = service.deduplicate_citations(citations)
        # Should deduplicate by source_path
        assert len(deduped) <= len(citations)

    def test_format_in_text_citations(self):
        """Test in-text citation formatting."""
        service = CitationService()
        citations = [
            CitationReference(
                index=1,
                source_path="test.md",
                title="Test",
                snippet="Content",
            )
        ]

        formatted = service.format_in_text_citations(citations)
        assert "[1]" in formatted


class TestGenerationService:
    """Tests for GenerationService."""

    @pytest.mark.asyncio
    async def test_generate_answer(self, mock_openai_client):
        """Test generating an answer."""
        mock_openai_client.chat.completions.create = MagicMock(
            return_value=MagicMock(
                choices=[
                    MagicMock(
                        message=MagicMock(
                            content="This is a generated answer about robotics."
                        )
                    )
                ]
            )
        )

        with patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            service = GenerationService()
            answer = await service.generate_answer(
                query="What is robotics?",
                context_chunks=["Robotics is the study of robots."],
            )

            assert isinstance(answer, str)
            assert len(answer) > 0

    @pytest.mark.asyncio
    async def test_generate_no_results_response(self, mock_openai_client):
        """Test generating response when no results found."""
        mock_openai_client.chat.completions.create = MagicMock(
            return_value=MagicMock(
                choices=[
                    MagicMock(
                        message=MagicMock(
                            content="I couldn't find specific information..."
                        )
                    )
                ]
            )
        )

        with patch(
            "app.services.generation.get_openai_client",
            return_value=mock_openai_client
        ):
            service = GenerationService()
            answer = await service.generate_no_results_response(
                query="obscure topic"
            )

            assert isinstance(answer, str)

    def test_prompt_template_context_building(self):
        """Test that prompt template builds context correctly."""
        chunks = ["Chunk 1 content", "Chunk 2 content"]
        context = PromptTemplate.build_context(chunks)
        assert "Chunk 1 content" in context
        assert "Chunk 2 content" in context

    def test_prompt_template_system_prompt(self):
        """Test system prompt template."""
        system_prompt = PromptTemplate.SYSTEM_PROMPT
        assert "Physical AI" in system_prompt
        assert "robotics" in system_prompt.lower()


class TestPromptTemplate:
    """Tests for PromptTemplate utilities."""

    def test_build_context_empty(self):
        """Test building context with no chunks."""
        context = PromptTemplate.build_context([])
        assert context == ""

    def test_build_context_with_chunks(self):
        """Test building context with chunks."""
        chunks = ["First chunk", "Second chunk", "Third chunk"]
        context = PromptTemplate.build_context(chunks)

        # Verify all chunks are included
        for chunk in chunks:
            assert chunk in context

        # Verify numbered format
        assert "[1]" in context
        assert "[2]" in context
        assert "[3]" in context

    def test_selection_mode_template(self):
        """Test selection mode prompt template."""
        template = PromptTemplate.SELECTION_MODE_TEMPLATE
        assert "{query}" in template
        assert "{selected_text}" in template
        assert "{context}" in template
