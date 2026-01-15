"""
Content indexing script.

Walks through the docs/ directory, parses markdown files,
generates embeddings, and uploads chunks to Qdrant.
"""

import asyncio
import logging
import os
import time
import uuid
from pathlib import Path
from typing import List, Dict, Any

import httpx

from app.db.qdrant import get_qdrant_service, TEXTBOOK_CHUNKS_COLLECTION
from app.services.chunking import get_chunking_service
from app.services.embedding import get_embedding_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Repository root
REPO_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = REPO_ROOT / "docs"

# Paths to index
INCLUDE_PATTERNS = [
    "module*/**/*.md",
]

# Paths to exclude
EXCLUDE_PATTERNS = [
    "_*",
    "node_modules/**",
]


class ContentIndexer:
    """
    Indexes markdown content for RAG search.

    Walks through textbook content, chunks it semantically,
    generates embeddings, and stores in Qdrant.
    """

    def __init__(self) -> None:
        """Initialize the content indexer."""
        self.chunking_service = get_chunking_service()
        self.embedding_service = get_embedding_service()
        self.qdrant_service = get_qdrant_service()

    async def index_all(self, force: bool = False) -> Dict[str, Any]:
        """
        Index all textbook content.

        Args:
            force: Re-index even if already indexed

        Returns:
            Indexing result summary
        """
        start_time = time.time()
        total_chunks = 0
        modules_processed = []
        errors = []

        # Initialize Qdrant collection
        await self.qdrant_service.initialize_collection()

        # If force reindex, clear existing collection
        if force:
            logger.info("Clearing existing collection for re-indexing...")
            await self.qdrant_service.delete_collection()
            await self.qdrant_service.initialize_collection()

        # Find all markdown files
        markdown_files = self._find_markdown_files()
        logger.info(f"Found {len(markdown_files)} markdown files to index")

        # Process each file
        for file_path in markdown_files:
            try:
                chunks_data = await self._index_file(file_path)
                total_chunks += len(chunks_data)

                # Extract module name from path
                rel_path = file_path.relative_to(DOCS_DIR)
                module = rel_path.parts[0] if rel_path.parts else "unknown"
                if module not in modules_processed:
                    modules_processed.append(module)

            except Exception as e:
                error_msg = f"Failed to index {file_path}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)

        duration = time.time() - start_time

        result = {
            "total_chunks": total_chunks,
            "modules_processed": modules_processed,
            "errors": errors,
            "duration_seconds": duration,
            "timestamp": int(time.time()),
        }

        logger.info(f"Indexing complete: {total_chunks} chunks in {duration:.2f}s")
        return result

    def _find_markdown_files(self) -> List[Path]:
        """Find all markdown files to index."""
        markdown_files = []

        for pattern in INCLUDE_PATTERNS:
            for path in DOCS_DIR.glob(pattern):
                if path.is_file() and self._should_include(path):
                    markdown_files.append(path)

        return sorted(markdown_files)

    def _should_include(self, path: Path) -> bool:
        """Check if a file should be included in indexing."""
        # Check exclude patterns
        for pattern in EXCLUDE_PATTERNS:
            if pattern in path.as_posix():
                return False

        # Only process .md files
        return path.suffix == ".md"

    async def _index_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Index a single markdown file.

        Args:
            file_path: Path to markdown file

        Returns:
            List of chunk data dictionaries
        """
        logger.info(f"Indexing: {file_path.relative_to(REPO_ROOT)}")

        # Read markdown content
        with open(file_path, "r", encoding="utf-8") as f:
            markdown = f.read()

        # Get URL path for this content
        rel_path = file_path.relative_to(DOCS_DIR)
        url_path = f"/{rel_path.with_suffix('')}"

        # Chunk the content
        chunks = self.chunking_service.chunk_markdown(markdown, url_path)

        # Prepare chunks for upload
        chunks_data = []
        for chunk in chunks:
            # Generate embedding
            embedding = await self.embedding_service.generate_embedding(
                chunk["text"]
            )

            # Create chunk ID (deterministic UUID based on module_id and chunk_index)
            # This ensures same content gets same ID for re-indexing
            chunk_identifier = f"{chunk['module_id']}_{chunk['chunk_index']}"
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_identifier))

            chunks_data.append({
                "chunk_id": chunk_id,
                "embedding": embedding,
                "payload": {
                    "text": chunk["text"],
                    "module_id": chunk["module_id"],
                    "lesson_title": chunk["lesson_title"],
                    "section_heading": chunk.get("section_heading"),
                    "url_anchor": chunk["url_anchor"],
                    "chunk_index": chunk["chunk_index"],
                    "token_count": chunk["token_count"],
                },
            })

        # Upload to Qdrant
        if chunks_data:
            await self.qdrant_service.upsert_chunks(chunks_data)

        return chunks_data


async def main():
    """Main entry point for content indexing."""
    import argparse

    parser = argparse.ArgumentParser(description="Index textbook content for RAG search")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-index even if content already indexed",
    )
    args = parser.parse_args()

    indexer = ContentIndexer()
    result = await indexer.index_all(force=args.force)

    # Print summary
    print("\n" + "=" * 50)
    print("INDEXING SUMMARY")
    print("=" * 50)
    print(f"Total chunks indexed: {result['total_chunks']}")
    print(f"Modules processed: {', '.join(result['modules_processed'])}")
    print(f"Duration: {result['duration_seconds']:.2f} seconds")
    if result['errors']:
        print(f"Errors: {len(result['errors'])}")
        for error in result['errors'][:5]:
            print(f"  - {error}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
