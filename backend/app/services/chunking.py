"""
Content chunking service for RAG indexing.

Splits markdown content into semantically meaningful chunks
preserving paragraph structure and code blocks.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.services.embedding import get_embedding_service

logger = logging.getLogger(__name__)


# Target chunk size in tokens (OpenAI tokens)
MIN_CHUNK_TOKENS = 300
TARGET_CHUNK_TOKENS = 400
MAX_CHUNK_TOKENS = 500


@dataclass
class SectionPath:
    """
    Tracks the hierarchical section path during markdown parsing.

    Structure: module > lesson > section
    """

    module: str = ""
    lesson: str = ""
    section: str = ""

    def to_string(self) -> str:
        """Convert path to string representation."""
        parts = [p for p in [self.module, self.lesson, self.section] if p]
        return " > ".join(parts) if parts else ""

    def to_module_id(self) -> str:
        """
        Convert to module_id format (used in URLs).

        Example: "module1-ros2-fundamentals"
        """
        parts = [p for p in [self.module, self.lesson, self.section] if p]
        # Convert to URL-friendly format
        return "-".join(parts).lower().replace(" ", "-")


class ChunkingService:
    """
    Service for markdown-aware semantic chunking.

    Parses markdown files and splits content into chunks that:
    - Target 300-500 tokens
    - Never split code blocks
    - Preserve paragraph boundaries
    - Include section context in metadata
    """

    def __init__(self) -> None:
        """Initialize the chunking service."""
        self.embedding_service = get_embedding_service()

    def chunk_markdown(
        self,
        markdown: str,
        url_path: str,
    ) -> List[Dict[str, Any]]:
        """
        Split markdown content into semantically meaningful chunks.

        Args:
            markdown: Raw markdown content
            url_path: URL path for this content (for metadata)

        Returns:
            List of chunk dictionaries with text, metadata, and placeholder for embedding
        """
        # Parse markdown structure
        lines = markdown.split("\n")
        chunks = []

        # Track section path and current chunk content
        section_path = self._extract_section_path(url_path)
        current_chunk_text: List[str] = []
        current_tokens = 0
        chunk_index = 0

        # Parse line by line
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check for headings
            if stripped.startswith("#"):
                # Save current chunk if it has content
                if current_chunk_text:
                    chunk = self._create_chunk(
                        current_chunk_text,
                        section_path,
                        chunk_index,
                        url_path,
                    )
                    if chunk:
                        chunks.append(chunk)
                        chunk_index += 1
                        current_chunk_text = []
                        current_tokens = 0

                # Update section path from heading
                self._update_section_path(section_path, stripped)

            # Check for code blocks (fenced with ```)
            elif stripped.startswith("```"):
                # Find the end of the code block
                code_block_lines = [line]
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_block_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    code_block_lines.append(lines[i])  # Closing ```

                # Save current chunk before code block
                if current_chunk_text:
                    chunk = self._create_chunk(
                        current_chunk_text,
                        section_path,
                        chunk_index,
                        url_path,
                    )
                    if chunk:
                        chunks.append(chunk)
                        chunk_index += 1
                        current_chunk_text = []
                        current_tokens = 0

                # Code block becomes its own chunk
                code_chunk = self._create_code_chunk(
                    code_block_lines,
                    section_path,
                    chunk_index,
                    url_path,
                )
                if code_chunk:
                    chunks.append(code_chunk)
                    chunk_index += 1

            # Regular content line
            else:
                # Count tokens for this line
                line_tokens = self.embedding_service.count_tokens(line)

                # Check if adding this line would exceed max chunk size
                if current_tokens + line_tokens > MAX_CHUNK_TOKENS and current_chunk_text:
                    # Save current chunk
                    chunk = self._create_chunk(
                        current_chunk_text,
                        section_path,
                        chunk_index,
                        url_path,
                    )
                    if chunk:
                        chunks.append(chunk)
                        chunk_index += 1
                        current_chunk_text = []
                        current_tokens = 0

                current_chunk_text.append(line)
                current_tokens += line_tokens

            i += 1

        # Don't forget the last chunk
        if current_chunk_text:
            chunk = self._create_chunk(
                current_chunk_text,
                section_path,
                chunk_index,
                url_path,
            )
            if chunk:
                chunks.append(chunk)

        logger.info(f"Chunked markdown into {len(chunks)} chunks")
        return chunks

    def _extract_section_path(self, url_path: str) -> SectionPath:
        """Extract initial section path from URL path."""
        # Example URL: /module1-ros2/introduction
        parts = url_path.strip("/").split("/")

        section_path = SectionPath()
        if parts and parts[0].startswith("module"):
            section_path.module = parts[0]
            if len(parts) > 1:
                section_path.lesson = parts[1]

        return section_path

    def _update_section_path(self, section_path: SectionPath, heading: str) -> None:
        """Update section path based on markdown heading."""
        level = heading.count("#")
        text = heading.lstrip("#").strip()

        if level == 1:
            section_path.section = ""
            section_path.lesson = text
        elif level == 2:
            section_path.section = text
        # level 3+ headings don't change path

    def _create_chunk(
        self,
        lines: List[str],
        section_path: SectionPath,
        index: int,
        url_path: str,
    ) -> Optional[Dict[str, Any]]:
        """Create a chunk dictionary from text lines."""
        text = "\n".join(lines).strip()
        if not text:
            return None

        token_count = self.embedding_service.count_tokens(text)

        # Build URL anchor
        url_anchor = f"{url_path}"
        if section_path.section:
            # Add section as anchor
            section_anchor = section_path.section.lower().replace(" ", "-")
            section_anchor = "".join(c for c in section_anchor if c.isalnum() or c == "-")
            url_anchor += f"#{section_anchor}"

        return {
            "text": text,
            "module_id": section_path.to_module_id(),
            "lesson_title": section_path.lesson or "Unknown",
            "section_heading": section_path.section or None,
            "url_anchor": url_anchor,
            "chunk_index": index,
            "token_count": token_count,
        }

    def _create_code_chunk(
        self,
        lines: List[str],
        section_path: SectionPath,
        index: int,
        url_path: str,
    ) -> Optional[Dict[str, Any]]:
        """Create a chunk for a code block (never split)."""
        text = "\n".join(lines).strip()
        if not text:
            return None

        token_count = self.embedding_service.count_tokens(text)

        # Build URL anchor
        url_anchor = f"{url_path}#code-block-{index}"

        return {
            "text": text,
            "module_id": section_path.to_module_id(),
            "lesson_title": section_path.lesson or "Unknown",
            "section_heading": section_path.section or None,
            "url_anchor": url_anchor,
            "chunk_index": index,
            "token_count": token_count,
            "is_code": True,
        }


# Global service instance
_chunking_service: Optional[ChunkingService] = None


def get_chunking_service() -> ChunkingService:
    """Get the singleton chunking service instance."""
    global _chunking_service
    if _chunking_service is None:
        _chunking_service = ChunkingService()
    return _chunking_service
