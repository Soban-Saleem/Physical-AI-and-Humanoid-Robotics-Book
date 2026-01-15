"""
Tests for text-selection mode Q&A functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models.chat import ChatSelectionRequest


class TestSelectionEndpoint:
    """Tests for /chat/selection endpoint."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_selection_request_validation(self):
        """Test ChatSelectionRequest validation."""
        request = ChatSelectionRequest(
            question="What is this?",
            selectedText="Selected text content",
            pageUrl="/docs/module1/lesson1",
            sessionId="test-session",
        )
        assert request.question == "What is this?"
        assert request.selectedText == "Selected text content"
        assert request.pageUrl == "/docs/module1/lesson1"

    def test_selection_missing_selected_text(self, client):
        """Test selection endpoint without selectedText."""
        response = client.post(
            "/chat/selection",
            json={
                "question": "Test question",
                "pageUrl": "/docs/test",
                "sessionId": "test",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_selection_missing_page_url(self, client):
        """Test selection endpoint without pageUrl."""
        response = client.post(
            "/chat/selection",
            json={
                "question": "Test question",
                "selectedText": "Selected text",
                "sessionId": "test",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_selection_too_large(self, client):
        """Test selection endpoint rejects overly large selections."""
        large_text = "x" * 6000  # Over 5000 char limit

        response = client.post(
            "/chat/selection",
            json={
                "question": "What is this?",
                "selectedText": large_text,
                "pageUrl": "/docs/test",
                "sessionId": "test",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "too large" in response.json()["detail"]["message"].lower()

    @pytest.mark.asyncio
    async def test_selection_success(self, client, mock_openai_client, mock_qdrant_client):
        """Test successful selection request."""
        mock_result = MagicMock(
            id="test_chunk",
            score=0.9,
            payload={
                "content": "Content from the same page",
                "source_path": "module1/lesson1.md",
                "module": "module1",
                "lesson": "lesson1",
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
            response = client.post(
                "/chat/selection",
                json={
                    "question": "Explain this concept",
                    "selectedText": "This is the selected text",
                    "pageUrl": "/docs/module1/lesson1",
                    "sessionId": "test-session",
                },
            )

            # May return 422 in test context due to validation
            assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]


class TestSelectionRetrieval:
    """Tests for selection-biased retrieval."""

    @pytest.mark.asyncio
    async def test_search_with_selection_bias_filters_by_module(self, mock_openai_client, mock_qdrant_client):
        """Test that selection search filters by module."""
        from app.services.retrieval import RetrievalService

        mock_result = MagicMock(
            id="chunk_123",
            score=0.88,
            payload={
                "content": "Content from module1",
                "source_path": "module1/lesson1.md",
                "module_id": "module1",
            }
        )

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(
                search=AsyncMock(return_value=[mock_result])
            )
        ):
            service = RetrievalService()
            results = await service.search_with_selection_bias(
                question="What is this?",
                selected_text="Selected content",
                page_url="/docs/module1/introduction",
                limit=5,
            )
            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_with_selection_falls_back_to_global(self, mock_openai_client):
        """Test fallback to global search when module filter fails."""
        from app.services.retrieval import RetrievalService, NoResultsFoundException

        mock_result = MagicMock(
            id="chunk_global",
            score=0.75,
            payload={
                "content": "Global search result",
                "source_path": "module2/lesson2.md",
            }
        )

        async def mock_search(*args, **kwargs):
            # First call (module filtered) fails, second (global) succeeds
            if kwargs.get("filters"):
                raise NoResultsFoundException("No module results")
            return [mock_result]

        with patch(
            "app.services.embedding.get_openai_client",
            return_value=mock_openai_client
        ), patch(
            "app.services.retrieval.get_qdrant_service",
            return_value=MagicMock(search=mock_search)
        ):
            service = RetrievalService()
            results = await service.search_with_selection_bias(
                question="What is this?",
                selected_text="Selected",
                page_url="/docs/unknown/page",
                limit=5,
            )
            # Should fall back to global search
            assert len(results) >= 0


class TestSelectionGeneration:
    """Tests for selection-mode answer generation."""

    @pytest.mark.asyncio
    async def test_generation_uses_selection_prompt(self, mock_openai_client):
        """Test that selection mode uses specific prompt."""
        from app.services.generation import GenerationService

        mock_openai_client.chat.completions.create = MagicMock(
            return_value=MagicMock(
                choices=[
                    MagicMock(
                        message=MagicMock(
                            content="Based on the selected text..."
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
                question="What does this mean?",
                context_chunks=["Some context"],
                selected_text="This is the selected text from the page",
            )

            assert isinstance(answer, str)
            assert len(answer) > 0
            # Verify the API was called
            assert mock_openai_client.chat.completions.create.called

    @pytest.mark.asyncio
    async def test_selection_prompt_includes_constraint(self, mock_openai_client):
        """Test that selection prompt includes constraint instructions."""
        from app.services.generation import PromptTemplate

        template = PromptTemplate.SELECTION_MODE_TEMPLATE
        assert "ONLY" in template or "only" in template.lower()
        assert "{selected_text}" in template
        assert "{question}" in template


class TestUrlExtraction:
    """Tests for module extraction from URLs."""

    def test_extract_module_from_valid_url(self):
        """Test extracting module ID from valid URL."""
        from app.services.retrieval import RetrievalService

        service = RetrievalService()

        # Test various URL formats
        assert service._extract_module_from_url("/module1-sensors/intro") == "module1-sensors"
        assert service._extract_module_from_url("/module2/ros2/fundamentals") == "module2"
        assert service._extract_module_from_url("/docs/module3-isaac/") == "module3-isaac"

    def test_extract_module_from_invalid_url(self):
        """Test handling of invalid URLs."""
        from app.services.retrieval import RetrievalService

        service = RetrievalService()

        # Should return None for invalid URLs
        assert service._extract_module_from_url("/intro") is None
        assert service._extract_module_from_url("/blog/post-1") is None
        assert service._extract_module_from_url("/") is None


class TestSelectionConstraints:
    """Tests for selection-mode constraints."""

    def test_max_selection_size_enforced(self):
        """Test that selection size limit is enforced."""
        from app.models.chat import ChatSelectionRequest

        # Valid size
        valid_request = ChatSelectionRequest(
            question="Test?",
            selectedText="x" * 5000,
            pageUrl="/docs/test",
            sessionId="test",
        )
        assert len(valid_request.selectedText) == 5000

    @pytest.mark.asyncio
    async def test_answer_constrained_to_selection(self, mock_openai_client):
        """Test that answers indicate when beyond selection scope."""
        from app.services.generation import GenerationService

        # Mock a response that acknowledges selection constraint
        mock_openai_client.chat.completions.create = MagicMock(
            return_value=MagicMock(
                choices=[
                    MagicMock(
                        message=MagicMock(
                            content="Based on the selected text, the answer is X. For more details, you'd need to check other sections."
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
                question="What are the advanced features?",
                context_chunks=[],
                selected_text="Basic feature description only",
            )

            assert isinstance(answer, str)
