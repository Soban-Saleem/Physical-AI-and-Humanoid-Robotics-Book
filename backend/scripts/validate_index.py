#!/usr/bin/env python3
"""
Index Validation Script

Checks Qdrant collection health and content coverage.
Reports on missing content and search quality.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.embedding import get_embedding_service
from app.db.qdrant import get_qdrant_service
from app.core.config import get_settings

settings = get_settings()


# Expected modules and their keywords for coverage check
EXPECTED_MODULES = {
    "module1": ["physical ai", "sensors", "lidar", "imu", "camera"],
    "module2": ["ros 2", "nodes", "topics", "services", "actions"],
    "module3": ["gazebo", "simulation", "unity", "physics"],
    "module4": ["nvidia", "isaac", "isaac sim", "navigation"],
    "module5": ["kinematics", "locomotion", "manipulation", "hri"],
}


async def check_collection_health() -> Dict:
    """Check basic collection health metrics."""
    print("🏥 Checking collection health...")

    qdrant = get_qdrant_service()

    try:
        info = await qdrant.collection_info()

        return {
            "status": "healthy",
            "vectors_count": info.get("vectors_count", 0),
            "segments_count": info.get("segments_count", 0),
            "points_count": info.get("points_count", 0),
            "status_value": info.get("status", "unknown"),
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }


async def check_module_coverage() -> Dict[str, List[str]]:
    """Check which modules have content indexed."""
    print("\n📚 Checking module coverage...")

    qdrant = get_qdrant_service()
    embedding = get_embedding_service()

    coverage = {}

    for module, keywords in EXPECTED_MODULES.items():
        module_found = False

        for keyword in keywords[:2]:  # Check first 2 keywords per module
            try:
                query_embedding = await embedding.generate_embedding(keyword)
                results = await qdrant.search_chunks(
                    query_vector=query_embedding,
                    limit=1,
                    score_threshold=0.3,
                    filters={"module_id": module} if module else None,
                )

                if results:
                    module_found = True
                    break
            except Exception:
                pass

        coverage[module] = "found" if module_found else "missing"
        status_icon = "✓" if module_found else "✗"
        print(f"  {status_icon} {module}: {'Found' if module_found else 'Not found'}")

    return coverage


async def check_search_quality() -> Dict:
    """Test search quality with sample queries."""
    print("\n🔍 Testing search quality...")

    qdrant = get_qdrant_service()
    embedding = get_embedding_service()

    test_queries = [
        "What is ROS 2?",
        "How does LIDAR work?",
        "What is physical AI?",
        "Explain robot kinematics",
    ]

    results = {}

    for query in test_queries:
        try:
            query_embedding = await embedding.generate_embedding(query)
            search_results = await qdrant.search_chunks(
                query_vector=query_embedding,
                limit=3,
                score_threshold=0.0,
            )

            avg_score = 0
            if search_results:
                avg_score = sum(r.get("score", 0) for r in search_results) / len(search_results)

            results[query] = {
                "count": len(search_results),
                "avg_score": avg_score,
                "top_result": search_results[0].get("payload", {}).get("text", "")[:50] if search_results else None,
            }

            status = "✓" if len(search_results) > 0 and avg_score > 0.5 else "⚠"
            print(f"  {status} '{query}': {len(search_results)} results, avg score: {avg_score:.2f}")

        except Exception as e:
            results[query] = {"error": str(e)}
            print(f"  ✗ '{query}': Error - {e}")

    return results


async def check_content_distribution() -> Dict:
    """Analyze content distribution across modules."""
    print("\n📊 Analyzing content distribution...")

    qdrant = get_qdrant_service()

    # This is a simplified check - in production you'd aggregate properly
    try:
        info = await qdrant.collection_info()
        total_vectors = info.get("vectors_count", 0)

        if total_vectors == 0:
            return {"error": "No content indexed"}

        # Rough estimate: divide equally among expected modules
        per_module = total_vectors // len(EXPECTED_MODULES)

        print(f"  Total vectors: {total_vectors}")
        print(f"  Estimated per module: ~{per_module}")

        return {
            "total_vectors": total_vectors,
            "expected_modules": len(EXPECTED_MODULES),
            "estimated_per_module": per_module,
        }

    except Exception as e:
        return {"error": str(e)}


async def generate_recommendations(health: Dict, coverage: Dict, search_quality: Dict) -> List[str]:
    """Generate recommendations based on validation results."""
    recommendations = []

    if health.get("status") == "error":
        recommendations.append("❌ CRITICAL: Cannot connect to Qdrant. Check configuration.")
    elif health.get("vectors_count", 0) == 0:
        recommendations.append("❌ CRITICAL: Collection is empty. Run reindex.py to populate.")
    elif health.get("vectors_count", 0) < 100:
        recommendations.append("⚠️  WARNING: Low content count. Verify indexing completed.")

    missing_modules = [m for m, status in coverage.items() if status == "missing"]
    if missing_modules:
        recommendations.append(f"⚠️  Missing content for modules: {', '.join(missing_modules)}")

    poor_searches = [q for q, r in search_quality.items() if r.get("avg_score", 0) < 0.5 and "error" not in r]
    if poor_searches:
        recommendations.append(f"⚠️  Low search quality for: {', '.join(poor_searches)}")

    if not recommendations:
        recommendations.append("✅ All checks passed! Index looks healthy.")

    return recommendations


async def main():
    """Main validation entry point."""
    print("=" * 50)
    print("🔍 Qdrant Index Validation")
    print("=" * 50)

    # Run all checks
    health = await check_collection_health()
    coverage = await check_module_coverage()
    search_quality = await check_search_quality()
    distribution = await check_content_distribution()

    # Generate recommendations
    recommendations = await generate_recommendations(health, coverage, search_quality)

    # Print summary
    print("\n" + "=" * 50)
    print("📋 VALIDATION SUMMARY")
    print("=" * 50)

    print(f"\nCollection Status: {health.get('status', 'unknown').upper()}")
    print(f"Total Vectors: {health.get('vectors_count', 0)}")
    print(f"Modules Covered: {sum(1 for s in coverage.values() if s == 'found')}/{len(coverage)}")

    print("\n" + "=" * 50)
    print("💡 RECOMMENDATIONS")
    print("=" * 50)
    for rec in recommendations:
        print(f"  {rec}")

    # Exit with appropriate code
    if any("CRITICAL" in r for r in recommendations):
        print("\n❌ Validation FAILED")
        sys.exit(1)
    elif any("WARNING" in r for r in recommendations):
        print("\n⚠️  Validation passed with warnings")
        sys.exit(0)
    else:
        print("\n✅ Validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
