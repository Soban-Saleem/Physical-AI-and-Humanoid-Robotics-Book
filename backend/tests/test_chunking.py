"""
Tests for markdown-aware chunking service.
"""

import pytest
from unittest.mock import patch

from app.services.chunking import (
    ChunkingService,
    SectionPath,
    split_markdown_into_chunks,
    count_tokens,
)


class TestSectionPath:
    """Tests for SectionPath dataclass."""

    def test_section_path_creation(self):
        """Test creating a SectionPath."""
        path = SectionPath(module="module1", lesson="lesson1", section="intro")
        assert path.module == "module1"
        assert path.lesson == "lesson1"
        assert path.section == "intro"

    def test_section_path_to_string(self):
        """Test SectionPath to_string method."""
        path = SectionPath(module="module1", lesson="lesson1", section="intro")
        assert path.to_string() == "module1 > lesson1 > intro"


class TestTokenCounting:
    """Tests for token counting utility."""

    def test_count_tokens_simple_text(self):
        """Test counting tokens in simple text."""
        text = "This is a simple test with some words."
        count = count_tokens(text)
        assert count > 0
        assert count < 20  # Rough estimate

    def test_count_tokens_code(self):
        """Test counting tokens in code blocks."""
        code = "def hello():\n    print('world')"
        count = count_tokens(code)
        assert count > 0

    def test_count_tokens_empty(self):
        """Test counting tokens in empty string."""
        count = count_tokens("")
        assert count == 0


class TestSplitMarkdownIntoChunks:
    """Tests for markdown chunking function."""

    def test_chunk_simple_paragraph(self):
        """Test chunking a simple paragraph."""
        text = "This is a simple paragraph. It has multiple sentences. But not too long."
        chunks = split_markdown_into_chunks(
            text,
            source_path="test.md",
            section_path=SectionPath(module="test", lesson="test", section="test"),
            min_tokens=10,
            target_tokens=50,
            max_tokens=100,
        )
        assert len(chunks) > 0
        assert all(chunk.content for chunk in chunks)

    def test_chunk_preserves_code_blocks(self):
        """Test that code blocks are not split."""
        code_block = """
```python
def hello_world():
    print("Hello, world!")
    return True
```
"""
        chunks = split_markdown_into_chunks(
            code_block,
            source_path="test.md",
            section_path=SectionPath(module="test", lesson="test", section="test"),
            min_tokens=10,
            target_tokens=50,
            max_tokens=100,
        )
        assert len(chunks) == 1
        assert "```python" in chunks[0].content
        assert "```" in chunks[0].content

    def test_chunk_respects_max_tokens(self):
        """Test that chunks don't exceed max_tokens significantly."""
        long_text = " ".join(["word"] * 1000)  # Create a long text
        chunks = split_markdown_into_chunks(
            long_text,
            source_path="test.md",
            section_path=SectionPath(module="test", lesson="test", section="test"),
            min_tokens=50,
            target_tokens=100,
            max_tokens=150,
        )
        for chunk in chunks:
            token_count = count_tokens(chunk.content)
            # Allow some overflow for code blocks, but generally respect max
            if not "```" in chunk.content:
                assert token_count <= 200  # Allow some buffer

    def test_chunk_includes_metadata(self):
        """Test that chunks include proper metadata."""
        text = "Test content for metadata."
        chunks = split_markdown_into_chunks(
            text,
            source_path="module1/lesson1.md",
            section_path=SectionPath(module="module1", lesson="lesson1", section="intro"),
        )
        assert chunks[0].metadata.source_path == "module1/lesson1.md"
        assert chunks[0].metadata.section_path.module == "module1"
        assert chunks[0].metadata.section_path.lesson == "lesson1"


class TestChunkingService:
    """Tests for ChunkingService class."""

    def test_chunk_document_from_string(self):
        """Test chunking a document from string."""
        service = ChunkingService()
        markdown_content = """
# Introduction

This is the introduction section.

## Getting Started

Here is some getting started content.
"""
        result = service.chunk_document(
            content=markdown_content,
            source_path="test.md",
        )
        assert result.total_chunks > 0
        assert len(result.chunks) == result.total_chunks
        assert all(c.content for c in result.chunks)

    def test_chunk_document_empty_content(self):
        """Test chunking empty document."""
        service = ChunkingService()
        result = service.chunk_document(
            content="",
            source_path="test.md",
        )
        assert result.total_chunks == 0
        assert len(result.chunks) == 0

    def test_chunk_document_markdown_sections(self):
        """Test that markdown sections are tracked."""
        service = ChunkingService()
        markdown_content = """
# Module 1

Content for module 1.

## Lesson 1.1

Content for lesson 1.1.
"""
        result = service.chunk_document(
            content=markdown_content,
            source_path="module1/lesson1.md",
        )
        assert result.total_chunks > 0
        # Verify section metadata is populated
        assert any(
            c.metadata.section_path.module == "module1" for c in result.chunks
        )

    @patch('app.services.chunking.count_tokens')
    def test_chunk_service_uses_token_counter(self, mock_count_tokens):
        """Test that the service uses the token counter."""
        mock_count_tokens.return_value = 50
        service = ChunkingService()
        service.chunk_document(
            content="Test content",
            source_path="test.md",
        )
        # Verify count_tokens was called
        assert mock_count_tokens.call_count > 0
