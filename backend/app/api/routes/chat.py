"""
Chat endpoint for question-answering.

Handles /chat and /chat/selection endpoints for the RAG chatbot.
"""

import secrets
import time
import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models.chat import (
    ChatRequest,
    ChatResponse,
    ChatSelectionRequest,
    CitationReference,
)
from app.services.retrieval import get_retrieval_service
from app.services.generation import get_generation_service
from app.services.citation import get_citation_service
from app.services.embedding import get_embedding_service
from app.db.neon import get_neon_service
from app.api.dependencies import generate_cache_key
from app.core.exceptions import NoResultsFoundException, ServiceUnavailableException

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Answer a question about the textbook content.

    Uses RAG (Retrieval-Augmented Generation) to:
    1. Generate embedding for the question
    2. Search for relevant content chunks
    3. Generate answer using retrieved chunks as context
    4. Return answer with source citations

    Args:
        request: Chat request with question and optional context

    Returns:
        ChatResponse with answer and citations

    Raises:
        HTTPException: For validation or service errors
    """
    start_time = time.time()

    # Generate or get session ID
    session_id = request.sessionId or secrets.token_urlsafe(16)

    # Generate cache key
    cache_key = generate_cache_key(request.question)

    try:
        # Get services
        retrieval = get_retrieval_service()
        generation = get_generation_service()
        citation = get_citation_service()

        # Step 1: Search for relevant content
        search_results = await retrieval.search(
            question=request.question,
            limit=5,
            score_threshold=0.5,
        )

        # Step 2: Generate answer
        context_chunks = [result.text for result in search_results]

        answer = await generation.generate_answer(
            question=request.question,
            context_chunks=context_chunks,
            context_messages=request.contextMessages,
        )

        # Step 3: Format citations
        citations = citation.format_citations(search_results)

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Step 4: Log interaction (async, don't await)
        neon = get_neon_service()
        if neon.is_initialized():
            _ = neon.log_interaction(
                session_id=session_id,
                question=request.question,
                answer=answer,
                citations_count=len(citations),
                is_cached=False,
                response_time_ms=response_time_ms,
                module_id=_extract_module_id(citations),
            )

        return ChatResponse(
            answer=answer,
            citations=citations,
            sessionId=session_id,
            isCached=False,
        )

    except NoResultsFoundException as e:
        # Generate helpful no-results response
        generation = get_generation_service()
        answer = await generation.generate_no_results_response(
            question=request.question,
            suggested_topics=e.suggested_topics,
        )

        return ChatResponse(
            answer=answer,
            citations=[],
            sessionId=session_id,
            isCached=False,
        )

    except ServiceUnavailableException as e:
        # Include retry information in response
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "ServiceUnavailable",
                "message": e.message,
                "retry_after": getattr(e, "retry_after", 30),
            },
        )

    except Exception as e:
        logger.exception(f"Unexpected error in /chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
            },
        )


@router.post("/selection", response_model=ChatResponse)
async def chat_selection(request: ChatSelectionRequest) -> ChatResponse:
    """
    Answer a question based on selected text from the page.

    This endpoint constrains the answer to use primarily the
    text that the user has selected on the page.

    Args:
        request: Chat selection request with selected text

    Returns:
        ChatResponse with answer constrained to selection

    Raises:
        HTTPException: For validation or service errors
    """
    start_time = time.time()

    # Generate or get session ID
    session_id = request.sessionId or secrets.token_urlsafe(16)

    # Validate selection size
    if len(request.selectedText) > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationException",
                "message": "Selected text is too large. Please select a smaller portion.",
            },
        )

    try:
        # Get services
        retrieval = get_retrieval_service()
        generation = get_generation_service()
        citation = get_citation_service()

        # Search with selection bias
        search_results = await retrieval.search_with_selection_bias(
            question=request.question,
            selected_text=request.selectedText,
            page_url=request.pageUrl,
            limit=5,
        )

        # Generate answer with selection mode prompt
        context_chunks = [result.text for result in search_results]

        answer = await generation.generate_answer(
            question=request.question,
            context_chunks=context_chunks,
            selected_text=request.selectedText,
        )

        # Format citations
        citations = citation.format_citations(search_results)

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Log interaction
        neon = get_neon_service()
        if neon.is_initialized():
            _ = neon.log_interaction(
                session_id=session_id,
                question=request.question,
                answer=answer,
                citations_count=len(citations),
                is_cached=False,
                response_time_ms=response_time_ms,
                module_id=_extract_module_id(citations),
            )

        return ChatResponse(
            answer=answer,
            citations=citations,
            sessionId=session_id,
            isCached=False,
        )

    except NoResultsFoundException as e:
        # For selection mode, be more specific about the limitation
        generation = get_generation_service()

        return ChatResponse(
            answer=f"""I couldn't find enough information in the selected text to answer "{request.question[:50]}...".

**Try this:**
- Expand your selection to include more context
- Ask your question without selecting text to search the entire textbook
- Check if the answer might be in a different section""",
            citations=[],
            sessionId=session_id,
            isCached=False,
        )

    except ServiceUnavailableException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "ServiceUnavailable",
                "message": e.message,
                "retry_after": getattr(e, "retry_after", 30),
            },
        )

    except Exception as e:
        logger.exception(f"Unexpected error in /chat/selection: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
            },
        )


def _extract_module_id(citations: List[CitationReference]) -> str | None:
    """Extract primary module ID from citations."""
    if citations:
        return citations[0].moduleId
    return None
