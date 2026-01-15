"""
Citation formatting service.

Converts Qdrant search results into properly formatted
citation references for chatbot responses.
"""

import logging
from typing import List, Any
from urllib.parse import urlencode

from app.models.chat import CitationReference
from app.models.document import SearchResult

logger = logging.getLogger(__name__)


class CitationService:
    """
    Service for formatting and managing citations.

    Takes raw search results from Qdrant and converts them
    into user-friendly citation references.
    """

    def format_citations(
        self,
        search_results: List[SearchResult],
    ) -> List[CitationReference]:
        """
        Convert search results to citation references.

        Args:
            search_results: List of search results from Qdrant

        Returns:
            List of formatted citation references
        """
        citations = []

        for i, result in enumerate(search_results):
            # Generate a unique citation ID
            citation_id = f"cite_{i:03d}_{result.chunk_id[:8]}"

            citation = CitationReference(
                citationId=citation_id,
                moduleId=result.metadata.module_id,
                lessonTitle=result.metadata.lesson_title,
                sectionHeading=result.metadata.section_heading,
                urlAnchor=self._build_url_anchor(result),
                relevanceScore=result.score,
            )

            citations.append(citation)

        logger.debug(f"Formatted {len(citations)} citations")
        return citations

    def _build_url_anchor(
        self,
        result: SearchResult,
    ) -> str:
        """
        Build a URL anchor for the citation link.

        Args:
            result: Search result with metadata

        Returns:
            URL anchor string
        """
        base_url = result.metadata.url_anchor

        # If URL doesn't start with /, prepend it
        if not base_url.startswith("/"):
            base_url = f"/{base_url}"

        # Add section anchor if available
        section = result.metadata.section_heading
        if section:
            # Convert section heading to URL-friendly anchor
            anchor = section.lower().replace(" ", "-").replace("/", "-")
            # Remove non-alphanumeric characters except hyphens
            anchor = "".join(
                c for c in anchor
                if c.isalnum() or c == "-"
            )
            base_url = f"{base_url.rsplit('#', 1)[0]}#{anchor}"

        return base_url

    def format_citation_text(
        self,
        citation: CitationReference,
    ) -> str:
        """
        Format a citation for inline display in responses.

        Args:
            citation: Citation to format

        Returns:
            Formatted citation text
        """
        parts = [citation.lessonTitle]

        if citation.sectionHeading:
            parts.append(f"({citation.sectionHeading})")

        return " - ".join(parts)

    def deduplicate_citations(
        self,
        citations: List[CitationReference],
    ) -> List[CitationReference]:
        """
        Remove duplicate citations based on URL anchor.

        Keeps the citation with the highest relevance score.

        Args:
            citations: List of citations (may have duplicates)

        Returns:
            Deduplicated citations
        """
        # Group by URL anchor
        anchor_map: dict[str, CitationReference] = {}

        for citation in citations:
            anchor = citation.urlAnchor
            existing = anchor_map.get(anchor)

            # Keep the one with higher score
            if existing is None or citation.relevanceScore > existing.relevanceScore:
                anchor_map[anchor] = citation

        result = list(anchor_map.values())
        # Sort by relevance score descending
        result.sort(key=lambda c: c.relevanceScore, reverse=True)

        removed = len(citations) - len(result)
        if removed > 0:
            logger.debug(f"Removed {removed} duplicate citations")

        return result

    def format_in_text_citations(
        self,
        citations: List[CitationReference],
        max_display: int = 3,
    ) -> str:
        """
        Format citations for display at the end of a chatbot response.

        Args:
            citations: List of citations to format
            max_display: Maximum number of citations to display

        Returns:
            Formatted citation text for appending to responses
        """
        if not citations:
            return ""

        # Take only the top N citations
        top_citations = citations[:max_display]

        lines = ["\n\n**Sources:**"]
        for citation in top_citations:
            parts = [f"- [{citation.lessonTitle}"]
            if citation.sectionHeading:
                parts.append(citation.sectionHeading)
            parts.append(f"]({citation.urlAnchor})")
            lines.append("".join(parts))

        if len(citations) > max_display:
            lines.append(f"\n*...and {len(citations) - max_display} more sources*")

        return "\n".join(lines)

    def extract_module_info(
        self,
        citations: List[CitationReference],
    ) -> dict[str, Any]:
        """
        Extract module-level information from citations.

        Args:
            citations: List of citations

        Returns:
            Dictionary with module breakdown
        """
        module_counts: dict[str, int] = {}
        modules: dict[str, str] = {}  # module_id -> display name

        for citation in citations:
            module_id = citation.moduleId
            module_counts[module_id] = module_counts.get(module_id, 0) + 1

            # Extract display name from module ID
            if module_id not in modules:
                modules[module_id] = module_id.replace("-", " ").title()

        return {
            "modules": modules,
            "counts": module_counts,
            "primary_module": max(module_counts, key=module_counts.get) if module_counts else None,
        }


# Global service instance
_citation_service: CitationService | None = None


def get_citation_service() -> CitationService:
    """
    Get the singleton citation service instance.

    Returns:
        CitationService: Active citation service
    """
    global _citation_service
    if _citation_service is None:
        _citation_service = CitationService()
    return _citation_service
