"""
Qdrant collection seeding script.

Initializes the textbook_chunks collection and validates the schema.
"""

import asyncio
import logging

from app.db.qdrant import get_qdrant_service, TEXTBOOK_CHUNKS_COLLECTION
from app.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize and validate Qdrant collection."""
    settings = get_settings()

    print("=" * 50)
    print("QDRANT COLLECTION INITIALIZATION")
    print("=" * 50)
    print(f"Qdrant URL: {settings.QDRANT_URL}")
    print(f"Collection: {TEXTBOOK_CHUNKS_COLLECTION}")
    print(f"Embedding Dimensions: 1536 (text-embedding-3-small)")
    print(f"Distance Metric: cosine")
    print("=" * 50)

    qdrant = get_qdrant_service()

    try:
        # Initialize collection
        success = await qdrant.initialize_collection()

        if success:
            print(f"✅ Collection '{TEXTBOOK_CHUNKS_COLLECTION}' is ready")

            # Get and display collection info
            info = await qdrant.collection_info()
            print(f"\nCollection Info:")
            print(f"  Name: {info['name']}")
            print(f"  Vectors Count: {info.get('vectors_count', 0)}")
            print(f"  Dimensions: {info['dimensions']}")
            print(f"  Distance: {info['distance']}")
            print(f"  Ready: {info.get('collection_ready', False)}")

            # Verify configuration
            assert info['dimensions'] == 1536, "Unexpected dimensions!"
            print("\n✅ Collection configuration validated")
        else:
            print("❌ Failed to initialize collection")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.exception("Collection initialization failed")


if __name__ == "__main__":
    asyncio.run(main())
