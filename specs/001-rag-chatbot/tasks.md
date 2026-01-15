# Tasks: Integrated RAG Chatbot for Physical AI Textbook

**Branch**: `001-rag-chatbot` | **Date**: 2025-01-15
**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [data-model.md](./data-model.md), [contracts/api.yaml](./contracts/api.yaml)

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, Foundation)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Frontend**: `src/chatbot/` for React components
- **Scripts**: `backend/scripts/` for indexing and utilities

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure in `backend/` with `app/`, `scripts/`, `tests/` folders per plan.md
- [X] T002 Create frontend chatbot directory structure in `src/chatbot/` with `bootstrap.js`, `SidebarChatbot.tsx`, `ChatInterface.tsx`, `useChat.ts`, `services/`, `types.ts`
- [X] T003 [P] Create `backend/requirements.txt` with FastAPI, uvicorn, httpx, qdrant-client, openai, psycopg2-binary, python-dotenv, tiktoken, pydantic, pytest, pytest-asyncio; create `package.json` for frontend with react-syntax-highlighter
- [X] T004 [P] Create `backend/pyproject.toml` with project metadata and pytest configuration
- [X] T005 [P] Create `backend/tests/conftest.py` with pytest fixtures for Qdrant, OpenAI, and Neon mocks
- [X] T006 [P] Create `src/chatbot/types.ts` with TypeScript interfaces: ChatSession, ChatMessage, CitationReference, CachedResponse

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Configuration & Environment

- [X] T007 Create `backend/app/core/config.py` with pydantic Settings for QDRANT_URL, QDRANT_API_KEY, OPENAI_API_KEY, NEON_DATABASE_URL, CORS_ORIGINS
- [X] T008 Create `backend/.env.example` with all required environment variables documented
- [X] T009 [P] Create `backend/app/core/exceptions.py` with custom exceptions: ServiceUnavailableException, RateLimitException, NoResultsFoundException

### Database Connections

- [X] T010 Create `backend/app/db/qdrant.py` with QdrantClient initialization and `textbook_chunks` collection setup (1536-dim vectors, cosine distance)
- [X] T011 [P] Create `backend/app/db/neon.py` with psycopg2 connection pool and interaction_log table creation

### API Framework

- [X] T012 Create `backend/app/main.py` with FastAPI app, CORS middleware configuration, and route registration
- [X] T013 [P] Create `backend/app/api/dependencies.py` with shared dependency injection for rate limiting and request validation

### Data Models

- [X] T014 Create `backend/app/models/chat.py` with Pydantic models: ChatRequest, ChatResponse, ChatSelectionRequest, CitationReference
- [X] T015 [P] Create `backend/app/models/document.py` with Pydantic models: ContentChunk, ChunkMetadata

### Core Services (Foundation)

- [X] T016 Create `backend/app/services/embedding.py` with `generate_embedding()` using OpenAI `text-embedding-3-small` (1536 dimensions)
- [X] T017 Create `backend/app/services/retrieval.py` with `search_chunks()` for Qdrant vector search (top 3-5 chunks)
- [X] T018 [P] Create `backend/app/services/citation.py` with `format_citations()` to convert Qdrant payloads to CitationReference objects

### Health Endpoint

- [X] T019 Create `backend/app/api/routes/health.py` with `/health` endpoint checking Qdrant, OpenAI, and Neon connectivity

### Tests (Foundation)

- [X] T020 [P] Create `backend/tests/test_config.py` verifying environment variable loading and validation
- [X] T021 [P] Create `backend/tests/test_health.py` verifying `/health` endpoint returns service status

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Questions About Course Content (Priority: P1) 🎯 MVP

**Goal**: Students can ask natural language questions and receive answers based on textbook content with source citations.

**Independent Test**: Index a sample lesson, ask "What is LIDAR?" and receive an answer citing Module 1 with lesson/section reference.

### Content Indexing

- [ ] T022 [P] [US1] Create `backend/app/services/chunking.py` with markdown-aware semantic chunking: parse AST, preserve paragraphs, target 300-500 tokens, never split code blocks
- [ ] T023 [US1] Create `backend/app/services/chunking.py` token counter using tiktoken cl100k_base encoding
- [ ] T024 [US1] Create `backend/app/services/chunking.py` section path tracking (module > lesson > section) for metadata
- [ ] T025 [US1] Create `backend/scripts/index_content.py` that walks `docs/`, parses markdown files, generates embeddings, uploads to Qdrant with metadata
- [ ] T026 [US1] Create `backend/scripts/seed_qdrant.py` to initialize `textbook_chunks` collection and validate schema

### Generation Service

- [ ] T027 [US1] Create `backend/app/services/generation.py` with `generate_answer()` using GPT-4o mini with retrieved chunks as context
- [ ] T028 [US1] Create `backend/app/services/generation.py` prompt template that enforces "answer ONLY from provided context" constraint with fallback for no-results case

### Chat Endpoint

- [ ] T029 [US1] Create `backend/app/api/routes/chat.py` with `POST /chat` endpoint: generate question embedding, search Qdrant, generate answer, format citations
- [ ] T030 [US1] Add error handling to `/chat`: ServiceUnavailableException with retry-after header, RateLimitException with 429 status, NoResultsFoundException with helpful message
- [ ] T031 [US1] Add request validation to `/chat`: max 5000 char questions, rate limiting per session

### Frontend Chat Widget

- [ ] T032 [P] [US1] Create `src/chatbot/ChatInterface.tsx` with message list, input field, send button, loading state, error display
- [ ] T033 [P] [US1] Create `src/chatbot/ChatInterface.tsx` citation rendering with links to source lessons/sections
- [ ] T033a [P] [US1] Add syntax highlighting to code blocks in ChatInterface.tsx citations using react-syntax-highlighter or Prism.js
- [ ] T034 [US1] Create `src/chatbot/SidebarChatbot.tsx` collapsible right sidebar panel (default collapsed, expands on toggle)
- [ ] T035 [US1] Add mobile responsive behavior to SidebarChatbot: full-screen overlay below 768px width with close button
- [ ] T036 [US1] Create `src/chatbot/useChat.ts` React hook with message state, loading state, error state, sendQuestion function

### API Client

- [ ] T037 [US1] Create `src/chatbot/services/api.ts` with `chat()` function using fetch with POST to `/chat`, JSON request/response
- [ ] T038 [US1] Add exponential backoff retry logic to `api.ts` (3 retries with 100ms → 200ms → 400ms delays)
- [ ] T038a [US1] Add "Clear history" button to ChatInterface.tsx that calls storage.clearSession() and resets message state

### Browser Storage

- [ ] T039 [P] [US1] Create `src/chatbot/services/storage.ts` with `saveSession()`, `loadSession()`, `clearSession()` using localStorage
- [ ] T040 [P] [US1] Create `src/chatbot/services/cache.ts` with IndexedDB wrapper for CachedResponse storage with 24-hour TTL

### Integration

- [ ] T041 [US1] Create `src/chatbot/bootstrap.js` client module entry point for Docusaurus integration
- [ ] T042 [US1] Update `docusaurus.config.js` to register client module: `clientModules: [require.resolve('./src/chatbot/bootstrap.js')]`

### Tests (US1)

- [ ] T043 [P] [US1] Create `backend/tests/test_chunking.py` verifying markdown parser preserves structure, chunks are 300-500 tokens, code blocks not split
- [ ] T044 [P] [US1] Create `backend/tests/test_services.py` mocking OpenAI and Qdrant, verifying embedding generation and retrieval
- [ ] T045 [P] [US1] Create `backend/tests/test_api.py` for `/chat` endpoint with mocked services
- [ ] T046 [P] [US1] Create `backend/tests/test_integration.py` end-to-end: indexed content → question → embedding → retrieval → generation → citation

**Checkpoint**: User Story 1 complete - students can ask questions and receive cited answers

---

## Phase 4: User Story 2 - Text-Selection-Aware Q&A (Priority: P2)

**Goal**: Students can highlight specific text and ask questions constrained to that selection.

**Independent Test**: Highlight a paragraph about DH parameters, ask "Explain this", receive answer using only highlighted text.

### Text Selection Detection

- [ ] T047 [P] [US2] Create `src/chatbot/hooks/useTextSelection.ts` with `getSelection()` using `window.getSelection()` API
- [ ] T048 [P] [US2] Create `src/chatbot/hooks/useTextSelection.ts` with selection change detection and "Ask about selection" button visibility

### Backend Selection Endpoint

- [ ] T049 [US2] Create `backend/app/api/routes/chat.py` with `POST /chat/selection` endpoint accepting `{question, selected_text, page_url}`
- [ ] T050 [US2] Implement selection-mode retrieval in `/chat/selection`: filter chunks by page_url module/lesson, bias scoring toward selected text similarity
- [ ] T051 [US2] Add validation to `/chat/selection`: max 5000 chars selected_text, reject if selection too large (>3 chunks equivalent)

### Frontend Selection UI

- [ ] T052 [US2] Add "Ask about selection" floating button to SidebarChatbot.tsx that appears when text is selected
- [ ] T053 [US2] Create selection mode indicator in ChatInterface.tsx showing "Constraining to selection" when active
- [ ] T054 [US2] Add "clear selection" action to return to normal Q&A mode

### Selection Prompt Engineering

- [ ] T055 [US2] Update `backend/app/services/generation.py` with selection-mode prompt: "Answer ONLY using the selected text below. If answer requires knowledge beyond selection, indicate that clearly."

### Tests (US2)

- [ ] T056 [P] [US2] Create `backend/tests/test_selection.py` verifying `/chat/selection` constrains answers to selected text
- [ ] T057 [P] [US2] Create `src/chatbot/tests/useTextSelection.test.ts` verifying selection detection works across page content

**Checkpoint**: User Story 2 complete - text-selection-aware Q&A functional

---

## Phase 5: User Story 3 - Conversation Context Memory (Priority: P3)

**Goal**: Chatbot maintains conversational context for follow-up questions.

**Independent Test**: Ask "What is LIDAR?", follow up with "What are its limitations?", verify "its" refers to LIDAR.

### Context Window Management

- [ ] T058 [P] [US3] Create `src/chatbot/services/context.ts` with sliding window context: last 10 message IDs stored in ChatSession.contextWindow
- [ ] T059 [P] [US3] Update `src/chatbot/types.ts` ChatSession interface to include contextWindow: string[] with max 10 entries
- [ ] T060 [US3] Update `src/chatbot/useChat.ts` to maintain contextWindow array, trimming to last 10 on each message

### Backend Context Support

- [ ] T061 [US3] Update `backend/app/models/chat.py` ChatRequest to include optional `context_messages: List[ChatMessage]` field
- [ ] T062 [US3] Update `backend/app/services/generation.py` to include context messages in prompt when provided
- [ ] T063 [US3] Update `backend/app/api/routes/chat.py` to accept and pass context_messages to generation service

### Context Prompt Engineering

- [ ] T064 [US3] Update `backend/app/services/generation.py` prompt template with conversation history format: "Previous conversation:\n{context}\n\nCurrent question: {question}"

### Session State Persistence

- [ ] T065 [US3] Update `src/chatbot/services/storage.ts` `saveSession()` to persist contextWindow with messages
- [ ] T066 [US3] Update `src/chatbot/services/storage.ts` `loadSession()` to restore contextWindow on page navigation
- [ ] T067 [US3] Add session expiration handling: clear context if session older than 24 hours

### Tests (US3)

- [ ] T068 [P] [US3] Create `backend/tests/test_context.py` verifying context messages are included in generation prompt
- [ ] T069 [P] [US3] Create `src/chatbot/tests/context.test.ts` verifying sliding window trims to 10 messages

**Checkpoint**: User Story 3 complete - conversational context memory functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Error Handling & Retry Logic

- [ ] T070 [P] Add circuit breaker pattern to `src/chatbot/services/api.ts` after 5 consecutive failures
- [ ] T071 [P] Add retry queue to `src/chatbot/services/cache.ts` for failed requests during service unavailability

### Caching Enhancement

- [ ] T072 [P] [All] Implement semantic similarity fallback in `src/chatbot/services/cache.ts`: calculate embedding for cache miss, check for similar cached questions (>0.85 threshold)
- [ ] T073 [P] [All] Add cache hit tracking in CachedResponse with hit_count increment

### Accessibility

- [ ] T074 [P] Add ARIA labels to SidebarChatbot.tsx: `role="complementary"`, `aria-label="Course assistant chatbot"`
- [ ] T075 [P] Add keyboard navigation to ChatInterface.tsx: Tab to input, Enter to submit, Escape to close sidebar
- [ ] T076 [P] Add focus management: trap focus in sidebar when open, return focus to toggle button when closed

### Performance & Optimization

- [ ] T077 [P] Add request debouncing (300ms) to `src/chatbot/useChat.ts` sendQuestion function
- [ ] T078 [P] Implement lazy loading for SidebarChatbot.tsx: load widget JavaScript only when first toggled open
- [ ] T079 [P] Add code splitting to `src/chatbot/bootstrap.js` for async component loading

### Content Indexing Utilities

- [ ] T080 Create `backend/scripts/reindex.py` for manual full re-index with progress bar and validation
- [ ] T081 Create `backend/scripts/validate_index.py` to check Qdrant collection health and content coverage

### Analytics (Optional)

- [ ] T082 [P] Create `backend/app/services/analytics.py` with `log_interaction()` for anonymized Neon Postgres logging
- [ ] T083 [P] Integrate analytics logging into `/chat` and `/chat/selection` endpoints

### Documentation

- [ ] T084 Update [quickstart.md](./quickstart.md) with actual environment setup steps and local development URLs
- [ ] T085 Create `backend/README.md` with local development instructions and testing guidelines
- [ ] T085a Document manual frontend testing approach in `backend/README.md` (browser dev tools, responsive testing, accessibility audit with Lighthouse/Axe)

### Deployment Configuration

- [ ] T086 Create `backend/railway.json` for Railway deployment configuration (build command, start command)
- [ ] T087 Create `.github/workflows/deploy-backend.yml` for auto-deploy on push to 001-rag-chatbot branch

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - US1 (P1): Core Q&A - no dependencies on other stories
  - US2 (P2): Text selection - can develop alongside US1 after foundation
  - US3 (P3): Context memory - can develop alongside US1/US2 after foundation
- **Polish (Phase 6)**: Depends on desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 chat widget but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Extends US1 chat endpoint but independently testable

### Within Each User Story

- Content indexing before chat endpoint
- Core services before API routes
- Frontend components before integration
- Tests pass before story completion

### Parallel Opportunities

**Setup (Phase 1)**:
```bash
# All can run together:
T003: requirements.txt
T004: pyproject.toml
T005: conftest.py
T006: types.ts
```

**Foundational (Phase 2)**:
```bash
# Config & environment:
T009: exceptions.py
T011: neon.py
T018: citation.py

# Tests:
T020: test_config.py
T021: test_health.py
```

**User Story 1 (Phase 3)**:
```bash
# Chunking components:
T023: token counter
T024: section path tracking

# Frontend:
T032: ChatInterface message list
T033: ChatInterface citations

# Tests:
T043: test_chunking.py
T044: test_services.py
T045: test_api.py
```

**User Story 2 (Phase 4)**:
```bash
# Selection detection:
T047: getSelection()
T048: selection change detection

# Tests:
T056: test_selection.py
T057: useTextSelection.test.ts
```

**User Story 3 (Phase 5)**:
```bash
# Context components:
T058: sliding window
T059: ChatSession interface

# Tests:
T068: test_context.py
T069: context.test.ts
```

**Polish (Phase 6)**:
```bash
# All marked [P] can run together:
T070: circuit breaker
T071: retry queue
T072: semantic cache
T073: hit tracking
T074: ARIA labels
T075: keyboard nav
T076: focus management
T077: debouncing
T078: lazy loading
T082: analytics service
```

---

## Parallel Example: User Story 1 Implementation

```bash
# Launch all chunking tasks together (different functions in same file):
Task T023: "Create token counter using tiktoken"
Task T024: "Create section path tracking for metadata"

# Launch all frontend ChatInterface tasks together (different concerns):
Task T032: "Create ChatInterface with message list, input, send button"
Task T033: "Create ChatInterface citation rendering with links"

# Launch all storage/cache tasks together (different files):
Task T039: "Create storage.ts with localStorage functions"
Task T040: "Create cache.ts with IndexedDB wrapper"

# Launch all tests together (independent test files):
Task T043: "Create test_chunking.py"
Task T044: "Create test_services.py"
Task T045: "Create test_api.py"
Task T046: "Create test_integration.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T021) - CRITICAL
3. Complete Phase 3: User Story 1 (T022-T046)
4. **STOP and VALIDATE**: Test US1 independently with sample content
5. Deploy/demonstrate MVP if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Apply Polish → Final production release

### Parallel Team Strategy

With multiple developers after Foundational phase completes:

1. **Developer A**: User Story 1 (T022-T046) - Core Q&A
2. **Developer B**: User Story 2 (T047-T057) - Text selection
3. **Developer C**: User Story 3 (T058-T069) - Context memory

Stories complete and integrate independently, each adding value without breaking previous work.

---

## Notes

- **[P] tasks**: Different files or concerns, can run in parallel with careful coordination
- **[Story] label**: Maps task to specific user story for traceability from spec → tasks → code
- **Each user story** is independently completable and testable
- **Commit frequently**: After each task or logical group (e.g., all chunking tasks together)
- **Validate at checkpoints**: Stop after each user story phase to test independently
- **Avoid**: Vague tasks like "implement caching" - be specific with file paths and function names
