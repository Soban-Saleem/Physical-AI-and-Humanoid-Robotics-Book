"""
Answer generation service using OpenAI.

Generates responses to user questions based on retrieved
content chunks using GPT-4o mini.
"""

import logging
from typing import List, Optional

from openai import OpenAI, APIError, RateLimitError, APIConnectionError

from app.core.config import get_settings
from app.core.exceptions import ServiceUnavailableException
from app.models.chat import ChatMessage

logger = logging.getLogger(__name__)

settings = get_settings()


class PromptTemplate:
    """
    Prompt templates for answer generation.

    Ensures consistent, high-quality responses that only
    use the provided context.
    """

    SYSTEM_PROMPT = """You are a helpful teaching assistant for the "Physical AI & Humanoid Robotics" textbook.

Your role is to answer student questions about course material using ONLY the content provided below.

**Important Rules:**
1. Answer ONLY using the provided textbook content
2. If the answer cannot be found in the content, state clearly that the topic is not covered
3. Be concise but thorough - aim for 2-4 paragraphs
4. Include relevant technical details and examples from the content
5. Format code examples with appropriate syntax
6. Do NOT make up information or use external knowledge

**Response Format:**
- Start with a direct answer
- Include relevant details and explanations from the content
- End with a brief summary if helpful
- Use markdown formatting for readability"""

    CONTEXT_TEMPLATE = """**Relevant Textbook Content:**
{context_chunks}

**User Question:** {question}

**Your Answer:**"""

    NO_RESULTS_PROMPT = """I couldn't find specific information about that topic in the textbook.

Based on the course structure, this might be covered in a module you haven't reached yet, or it may be outside the scope of this course.

**Suggestions:**
- Try rephrasing your question
- Check the module list for related topics
{topic_suggestions}

Would you like me to help you find information on a related topic?"""

    SELECTION_MODE_TEMPLATE = """**Selected Text from Page:**
{selected_text}

**User Question:** {question}

**Instructions:**
Answer the question using ONLY the selected text above. If the answer requires knowledge beyond the selected text, clearly indicate that information.

**Your Answer:**"""

    CONVERSATION_CONTEXT_TEMPLATE = """**Previous Conversation:**
{conversation_history}

**Current Question:** {question}

**Relevant Textbook Content:**
{context_chunks}

**Your Answer:**"""


class GenerationService:
    """
    Service for generating chatbot responses using OpenAI.

    Takes retrieved content chunks and user questions, then
    generates contextual answers using GPT-4o mini.
    """

    def __init__(self) -> None:
        """Initialize the generation service."""
        self.settings = get_settings()
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        """Get or create the OpenAI client."""
        if self._client is None:
            self._client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        return self._client

    async def generate_answer(
        self,
        question: str,
        context_chunks: List[str],
        context_messages: Optional[List[ChatMessage]] = None,
        selected_text: Optional[str] = None,
    ) -> str:
        """
        Generate an answer to the user's question.

        Args:
            question: User's question
            context_chunks: Retrieved content chunks
            context_messages: Optional conversation history for context
            selected_text: Optional selected text for text-selection mode

        Returns:
            Generated answer text

        Raises:
            ServiceUnavailableException: If OpenAI API fails
            RateLimitException: If rate limit exceeded
        """
        try:
            # Build prompt based on mode
            if selected_text:
                prompt = self._build_selection_mode_prompt(question, selected_text)
            elif context_messages:
                prompt = self._build_context_prompt(
                    question,
                    context_chunks,
                    context_messages
                )
            else:
                prompt = self._build_standard_prompt(question, context_chunks)

            # Generate response
            response = self.client.chat.completions.create(
                model=self.settings.OPENAI_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": PromptTemplate.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.3,  # Lower for more factual responses
            )

            answer = response.choices[0].message.content.strip()
            logger.info(f"Generated answer with {len(answer)} characters")
            return answer

        except RateLimitException as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise RateLimitException(
                message="Response generation rate limit exceeded",
                retry_after=60,
            ) from e

        except (APIConnectionError, APIError) as e:
            logger.error(f"OpenAI API error: {e}")
            raise ServiceUnavailableException(
                message="Failed to generate response",
                service="openai",
                retry_after=30,
            ) from e

    async def generate_no_results_response(
        self,
        question: str,
        suggested_topics: List[str],
    ) -> str:
        """
        Generate a helpful response when no content is found.

        Args:
            question: User's question
            suggested_topics: Topics the user might want to explore

        Returns:
            Helpful message about no results found
        """
        topic_list = "\n".join(f"- {topic}" for topic in suggested_topics[:5])
        return PromptTemplate.NO_RESULTS_PROMPT.format(
            topic_suggestions=f"**Topics you might explore:**\n{topic_list}"
        )

    def _build_standard_prompt(
        self,
        question: str,
        context_chunks: List[str],
    ) -> str:
        """Build standard prompt with context chunks."""
        context_text = "\n\n---\n\n".join(
            f"[{i+1}] {chunk[:500]}..."
            for i, chunk in enumerate(context_chunks)
        )
        return PromptTemplate.CONTEXT_TEMPLATE.format(
            context_chunks=context_text,
            question=question,
        )

    def _build_selection_mode_prompt(
        self,
        question: str,
        selected_text: str,
    ) -> str:
        """Build prompt for text-selection mode."""
        # Truncate selected text if too long
        truncated = selected_text[:2000] if len(selected_text) > 2000 else selected_text
        return PromptTemplate.SELECTION_MODE_TEMPLATE.format(
            selected_text=truncated,
            question=question,
        )

    def _build_context_prompt(
        self,
        question: str,
        context_chunks: List[str],
        context_messages: List[ChatMessage],
    ) -> str:
        """Build prompt with conversation history."""
        # Format conversation history
        history_lines = []
        for msg in context_messages[-5:]:  # Last 5 messages
            role = "Student" if msg.messageType == "user" else "Assistant"
            content = msg.content[:200]  # Truncate for context
            history_lines.append(f"{role}: {content}...")

        history = "\n".join(history_lines)

        # Format context chunks
        context_text = "\n\n---\n\n".join(
            f"[{i+1}] {chunk[:500]}..."
            for i, chunk in enumerate(context_chunks)
        )

        return PromptTemplate.CONVERSATION_CONTEXT_TEMPLATE.format(
            conversation_history=history,
            question=question,
            context_chunks=context_text,
        )


# Global service instance
_generation_service: Optional[GenerationService] = None


def get_generation_service() -> GenerationService:
    """Get the singleton generation service instance."""
    global _generation_service
    if _generation_service is None:
        _generation_service = GenerationService()
    return _generation_service
