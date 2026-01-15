# Feature Specification: Integrated RAG Chatbot for Physical AI Textbook

**Feature Branch**: `001-rag-chatbot`
**Created**: 2025-01-15
**Status**: Clarified
**Input**: User description for Phase 2 RAG Chatbot Development

---

## Overview

An intelligent question-answering assistant embedded within the Physical AI & Humanoid Robotics textbook platform. The chatbot helps students learn by answering questions about course content, with the unique ability to focus responses on specific text selections made by the user.

---

## Scope Boundaries

### In Scope
- Question-answering about textbook content only (13 modules of course material)
- Text-selection-aware Q&A (user highlights text, bot answers based on selection)
- Chat interface as a collapsible right sidebar panel (default collapsed, expands on toggle)
- Response citations linking back to specific lessons/sections
- Anonymous sessions with browser-local storage

### Out of Scope
- General web search or external knowledge sources
- User account creation/authentication (anonymous sessions only)
- Admin dashboard for conversation monitoring
- Multi-language support (reserved for Phase 3 Urdu translation)
- Voice input/output (reserved for Module 13 - Conversational Robotics)
- Real-time collaboration features

---

## Clarifications

### Session 2025-01-15

- Q: Chat widget placement pattern → A: Collapsible right sidebar panel (default collapsed, expands on toggle)
- Q: Content chunking strategy for semantic search → A: Semantic paragraph chunks (300-500 tokens)
- Q: Service failure recovery behavior → A: Cached responses + retry queue (show cached similar answers if available, queue new questions for auto-retry)
- Q: Mobile/small screen behavior → A: Full-screen overlay (sidebar expands to cover viewport with close button on screens under 768px)
- Q: Number of content chunks to retrieve per query → A: Top 3-5 chunks (balanced quality, latency, and cost)

---

## User Scenarios & Testing

### User Story 1 - Ask Questions About Course Content (Priority: P1)

A student reading the textbook encounters a concept they don't fully understand. They want to ask a natural language question and receive an answer based on the course material, with a citation showing where the information came from.

**Why this priority**: This is the core value proposition - immediate learning assistance without leaving the textbook. Without this, there is no chatbot.

**Independent Test**: Can be fully tested by indexing a sample lesson and asking questions about its content. Successfully answers questions with source citations = viable MVP.

**Acceptance Scenarios**:

1. **Given** a student is viewing any lesson page, **When** they type "What is the difference between LIDAR and IMU?" in the chat, **Then** the system returns an answer explaining the difference based on Module 1 content and cites the specific lesson and section
2. **Given** a student asks about a topic not covered in the textbook, **When** the question is submitted, **Then** the system responds that the topic is not covered in the course material and suggests related topics that are covered
3. **Given** a student asks an ambiguous question, **When** multiple relevant sections exist, **Then** the system provides a comprehensive answer citing multiple sources

---

### User Story 2 - Text-Selection-Aware Q&A (Priority: P2)

A student is reading a complex paragraph about inverse kinematics and wants the chatbot to explain only that specific content, not draw from unrelated parts of the textbook.

**Why this priority**: This is a key differentiator that enables focused learning. Students want to understand specific concepts without getting confused by unrelated context. P2 because core Q&A must work first.

**Independent Test**: Can be tested by highlighting a specific paragraph and asking questions. System should answer using only the highlighted text as context.

**Acceptance Scenarios**:

1. **Given** a student has highlighted a paragraph about DH parameters, **When** they click "Ask about selection" and type "Explain this", **Then** the system provides an explanation based only on the highlighted text
2. **Given** a student highlights text about a topic, **When** they ask a question requiring knowledge beyond the selection, **Then** the system indicates the answer cannot be provided from the selected text alone and suggests expanding the selection or asking without selection
3. **Given** no text is currently selected, **When** the user clicks "Ask about selection", **Then** the system prompts them to first select text from the page

---

### User Story 3 - Conversation Context Memory (Priority: P3)

A student asks a follow-up question like "What about the quaternion version?" referring to their previous question about rotation matrices. The chatbot should understand the conversational context.

**Why this priority**: Improves user experience but basic Q&A (P1) and text-selection (P2) are more essential. Students can work around this by repeating context if needed.

**Independent Test**: Can be tested by having a conversation with multiple related questions and verifying the bot maintains context.

**Acceptance Scenarios**:

1. **Given** a student previously asked about rotation matrices, **When** they follow up with "What are the limitations of that approach?", **Then** the system interprets "that approach" as referring to rotation matrices
2. **Given** a conversation has exceeded 10 message exchanges, **When** the user asks a follow-up, **Then** the system maintains context from the most recent messages (sliding window)
3. **Given** a student starts a new session, **When** they send their first message, **Then** the system treats it as a fresh conversation without prior context

---

### Edge Cases

- **What happens when** the vector database returns no relevant content for a question?
  - System responds politely that the topic couldn't be found in the textbook and suggests asking about covered topics

- **What happens when** the AI service is unavailable or rate-limited?
  - System shows cached similar answers if available in local storage; new questions are queued locally and auto-retried when service recovers; user is notified of queued status

- **What happens when** a user highlights an extremely large portion of text (multiple pages)?
  - System prompts the user to select a smaller portion for best results

- **What happens when** the question is in a language other than English (before Phase 3 translation)?
  - System attempts to answer but may indicate that English is the primary supported language

- **What happens when** multiple students use the chatbot simultaneously?
  - Each session is isolated; users cannot see or access each other's conversations

- **What happens when** a student navigates to a different page during a conversation?
  - Chat history persists and the conversation context remains available

- **What happens when** the textbook content is updated?
  - The content index is refreshed to include new/updated material

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST index all textbook markdown content for semantic search
- **FR-002**: System MUST accept natural language questions from users
- **FR-003**: System MUST return answers based ONLY on textbook content (no external web search); retrieves top 3-5 most relevant content chunks per query for answer generation
- **FR-004**: System MUST cite the source of each answer with lesson and section references
- **FR-005**: System MUST provide a collapsible right sidebar panel (default collapsed, expands on toggle) for chat interface; on screens under 768px width, expands to full-screen overlay with close button
- **FR-006**: System MUST support questions based on user-selected text portions
- **FR-007**: System MUST maintain conversation context within a single session
- **FR-008**: System MUST display loading indicators while processing questions
- **FR-009**: System MUST store chat history locally in the user's browser
- **FR-010**: System MUST handle errors gracefully with user-friendly messages
- **FR-011**: System MUST display answers within 2 seconds of question submission
- **FR-012**: System MUST indicate when a question's topic is not covered in the textbook
- **FR-013**: System MUST allow users to clear their chat history
- **FR-014**: System MUST provide a toggle button to expand/collapse the sidebar panel
- **FR-015**: System MUST format code examples in answers using appropriate syntax highlighting
- **FR-016**: System MUST cache responses locally for offline fallback and common question acceleration

### Non-Functional Requirements

- **Performance**: First response appears within 2 seconds (FR-011 SLA); follow-up responses within 1 second is a goal (cached responses should be <500ms)
- **Availability**: Graceful degradation when external services are unavailable
- **Privacy**: No user PII is collected or stored; sessions are anonymous
- **Accessibility**: Chat interface must be keyboard navigable and screen reader compatible
- **Browser Support**: Works on modern browsers (Chrome, Firefox, Safari, Edge) released within last 2 years; responsive design supports mobile screens (full-screen overlay mode under 768px width)

### Key Entities

- **Chat Message**: Represents a single exchange between user and system. Contains message type (user/assistant), timestamp, content, and optional citation references.

- **Chat Session**: Represents a contiguous conversation between a user and the chatbot. Contains multiple messages, session ID, creation timestamp, and current context state.

- **Content Chunk**: Represents a semantically meaningful portion of indexed textbook content. Chunking strategy: semantic paragraphs of 300-500 tokens to preserve conceptual coherence. Contains the text, source location (module, lesson, section), and vector embedding for similarity search.

- **Citation Reference**: Links a chatbot response to its source material. Contains module identifier, lesson title, section heading, and URL anchor.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Students can ask a question and receive a cited answer within 2 seconds on 95% of attempts
- **SC-002**: 90% of answers correctly cite the specific lesson and section where information was found
- **SC-003**: When asked about covered topics, the chatbot provides relevant answers on at least 85% of questions
- **SC-004**: When a topic is not covered, the system correctly indicates this 100% of the time (no hallucination)
- **SC-005**: Text-selection mode correctly constrains answers to selected content on 90% of attempts
- **SC-006**: Chat interface is accessible and functional on all supported browsers and devices
- **SC-007**: System handles 50 concurrent users without performance degradation

### User Experience Goals

- Students find answers faster than searching through the textbook manually
- Answers help clarify concepts without requiring external sources
- Citation links enable students to navigate directly to relevant sections for deeper learning
- Chat interface is unobtrusive but easily accessible when needed

---

## Dependencies & Assumptions

### Dependencies
- Textbook content must be published and accessible for indexing
- External AI service (OpenAI API) for response generation
- Vector database service (Qdrant Cloud) for semantic search
- Database service (Neon Postgres) for anonymized analytics logging only (not session persistence)

### Assumptions
- Textbook content is primarily in English (Urdu translation is separate work)
- Students have modern web browsers with JavaScript enabled
- The course will not exceed Qdrant Cloud free tier limits (1 collection, reasonable vector count)
- OpenAI API usage will remain within acceptable cost boundaries for the project

---

## Technical Configuration Notes

**Note**: The following technical details are for implementation reference only and do not affect the specification's technology-agnostic requirements.

- **Vector Store**: Qdrant Cloud (Free Tier)
  - Cluster: e2bc507b-953a-453d-a847-735aa2ee1988
  - Endpoint: us-east4-0.gcp.cloud.qdrant.io:6333

- **Database**: Neon Serverless Postgres (Free Tier)
  - Connection via SSL required

- **AI Service**: OpenAI API
  - Model: GPT-4o mini (cost-effective for this use case)

- **Backend**: FastAPI
- **Frontend**: React components embedded in Docusaurus
