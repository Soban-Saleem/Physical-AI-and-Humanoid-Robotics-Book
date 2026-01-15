#!/usr/bin/env python3
"""
Manual Re-Indexing Script

Re-indexes all markdown content from the docs/ directory into Qdrant.
Displays progress bar and validates results.
"""

import asyncio
import sys
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.chunking import ChunkingService
from app.services.embedding import get_embedding_service
from app.db.qdrant import get_qdrant_service
from app.core.config import get_settings

try:
    from tqdm import tqdm
except ImportError:
    print("Installing tqdm for progress bar...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm import tqdm


settings = get_settings()


async def find_markdown_files(docs_path: Path) -> List[Path]:
    """Find all markdown files in the docs directory."""
    markdown_files = list(docs_path.rglob("*.md"))
    # Exclude index files and certain patterns
    excluded = {"_category_", "README", "index"}
    filtered = [
        f for f in markdown_files
        if not any(excluded in f.stem.lower() for excluded in excluded)
    ]
    return sorted(filtered)


async def index_file(file_path: Path, chunking_service: ChunkingService, embedding_service, qdrant_service):
    """Index a single markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        if not content.strip():
            return 0

        # Get relative path from docs/
        rel_path = str(file_path.relative_to(file_path.parents[1]))

        # Chunk the content
        chunking_result = chunking_service.chunk_document(
            content=content,
            source_path=rel_path,
        )

        if chunking_result.total_chunks == 0:
            return 0

        # Generate embeddings for all chunks
        chunks_text = [chunk.content for chunk in chunking_result.chunks]
        embeddings = await embedding_service.generate_embeddings_batch(chunks_text)

        # Prepare Qdrant points
        points = []
        for chunk, embedding in zip(chunking_result.chunks, embeddings):
            points.append({
                "id": f"{rel_path}::{chunk.metadata.chunk_index}",
                "vector": embedding,
                "payload": {
                    "text": chunk.content,
                    "source_path": rel_path,
                    "module_id": chunk.metadata.section_path.module,
                    "lesson_title": chunk.metadata.section_path.lesson,
                    "section_heading": chunk.metadata.section_path.section,
                    "url_anchor": f"/{rel_path}#{chunk.metadata.section_path.section}",
                    "chunk_index": chunk.metadata.chunk_index,
                    "token_count": chunk.metadata.token_count,
                }
            })

        # Upsert to Qdrant
        await qdrant_service.upsert_chunks(points)

        return chunking_result.total_chunks

    except Exception as e:
        print(f"\nError indexing {file_path}: {e}")
        return 0


async def reindex_all():
    """Re-index all markdown content with progress bar."""
    print("🔄 Starting full re-index...")
    print(f"Docs path: {Path('../docs').resolve()}")

    # Initialize services
    chunking_service = ChunkingService()
    embedding_service = get_embedding_service()
    qdrant_service = get_qdrant_service()

    # Check Qdrant connection
    print("\n📡 Checking Qdrant connection...")
    try:
        info = await qdrant_service.collection_info()
        print(f"✓ Qdrant connected. Collection: {info}")
    except Exception as e:
        print(f"✗ Qdrant connection failed: {e}")
        return

    # Find all markdown files
    docs_path = Path("../docs").resolve()
    print(f"\n🔍 Scanning for markdown files in {docs_path}...")
    files = await find_markdown_files(docs_path)
    print(f"✓ Found {len(files)} markdown files")

    if not files:
        print("No files to index!")
        return

    # Clear existing collection (optional - uncomment to reset)
    print("\n⚠️  Note: Existing data will be merged. To reset, delete the collection first.")

    # Index each file with progress bar
    total_chunks = 0
    successful_files = 0

    with tqdm(files, desc="Indexing files", unit="file") as pbar:
        for file_path in pbar:
            pbar.set_postfix_str(str(file_path.relative_to(docs_path))[:40])
            chunks = await index_file(file_path, chunking_service, embedding_service, qdrant_service)
            total_chunks += chunks
            if chunks > 0:
                successful_files += 1

    # Validate results
    print("\n\n📊 Indexing Summary:")
    print(f"  Files processed: {successful_files}/{len(files)}")
    print(f"  Total chunks indexed: {total_chunks}")

    # Get final collection stats
    try:
        info = await qdrant_service.collection_info()
        print(f"  Collection size: {info.get('vectors_count', 'unknown')} vectors")
    except Exception as e:
        print(f"  Warning: Could not fetch final stats: {e}")

    if total_chunks > 0:
        print("\n✅ Re-index complete!")
    else:
        print("\n⚠️  No content was indexed!")


async def validate_index():
    """Validate the indexed content."""
    print("\n🔍 Validating index...")

    qdrant_service = get_qdrant_service()

    try:
        info = await qdrant_service.collection_info()
        count = info.get("vectors_count", 0)

        if count == 0:
            print("✗ Collection is empty!")
            return False

        print(f"✓ Collection has {count} vectors")

        # Test a search query
        embedding_service = get_embedding_service()
        test_query = "What is ROS 2?"
        test_embedding = await embedding_service.generate_embedding(test_query)

        results = await qdrant_service.search_chunks(
            query_vector=test_embedding,
            limit=3,
            score_threshold=0.0,
        )

        print(f"✓ Test search returned {len(results)} results")

        if results:
            print("\n📝 Sample results:")
            for i, r in enumerate(results[:3], 1):
                payload = r.get("payload", {})
                print(f"  {i}. [{payload.get('module_id', 'N/A')}] {payload.get('text', '')[:60]}...")

        return True

    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Re-index textbook content into Qdrant")
    parser.add_argument("--validate-only", action="store_true", help="Only validate existing index")
    args = parser.parse_args()

    if args.validate_only:
        await validate_index()
    else:
        await reindex_all()
        await validate_index()


if __name__ == "__main__":
    asyncio.run(main())
