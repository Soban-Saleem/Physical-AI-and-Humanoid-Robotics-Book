# Implementation Plan: Integrated RAG Chatbot

**Branch**: `001-rag-chatbot` | **Date**: 2025-01-15 | **Spec**: [spec.md](./spec.md)

---

## Summary

Build an intelligent question-answering assistant embedded within the Physical AI & Humanoid Robotics textbook platform. The system uses RAG (Retrieval-Augmented Generation) to answer student questions about course content with source citations.

**Technical Approach**:
- **Content Indexing**: Parse markdown docs, chunk into 300-500 token paragraphs, generate embeddings via OpenAI `text-embedding-3-small`, store in Qdrant Cloud
- **Backend API**: FastAPI with `/chat` and `/chat/selection` endpoints, retrieves 3-5 relevant chunks, generates answers via GPT-4o mini
- **Frontend Widget**: React sidebar component (collapsible, mobile-responsive) injected into Docusaurus
- **Deployment**: Backend on Railway free tier, frontend on existing GitHub Pages

---

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5.3+, React 18
**Primary Dependencies**: FastAPI, OpenAI (GPT-4o mini, text-embedding-3-small), Qdrant Client, Docusaurus
**Storage**:
- Qdrant Cloud (Free Tier) - Vector store for content chunks
- Neon Postgres (Free Tier) - Optional analytics logging
- Browser localStorage - Chat sessions and response caching
**Testing**: pytest (backend), React Testing Library (frontend), Artillery for load testing
**Target Platform**:
- Backend: Railway (or Render) free tier container
- Frontend: GitHub Pages (static hosting)
- Browser: Chrome, Firefox, Safari, Edge (last 2 years)
**Project Type**: Web application (backend API + frontend widget)
**Performance Goals**:
- First response: <2 seconds (95th percentile)
- Follow-up responses: <1 second
- 50 concurrent users without degradation
**Constraints**:
- Free tier services only (Qdrant, Neon, Railway)
- Anonymous sessions (no auth)
- Browser-local storage (no server-side sessions)
- 2-second response time SLA
**Scale/Scope**:
- ~13 modules of textbook content
- Estimated 2,000-3,000 content chunks after indexing
- 50 concurrent users (free tier capacity)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Spec created via `/sp.specify`, clarified via `/sp.clarify` |
| II. Educational Quality | ⚠️ N/A | Platform feature (not educational content) |
| III. Technical Accuracy | ✅ PASS | Technical decisions verified against official docs (Qdrant, OpenAI, Docusaurus) |
| IV. Hardware-Awareness | ⚠️ N/A | Software-only feature |
| V. Subagent Orchestration | ⚠️ N/A | Platform implementation (not content) |

**Verdict**: No constitution violations. This is a platform feature, not educational content, so Principles II and V don't apply.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technical decisions (Phase 0)
├── data-model.md        # Entity definitions (Phase 1)
├── quickstart.md        # Developer onboarding (Phase 1)
├── contracts/           # API contracts (Phase 1)
│   └── api.yaml         # OpenAPI specification
└── tasks.md             # Implementation tasks (Phase 2 - /sp.tasks)
```

### Source Code (repository root)

**Structure Decision**: Option 2 - Web application (backend + frontend)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py  # Shared dependencies (CORS, etc.)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── chat.py      # /chat, /chat/selection endpoints
│   │       └── health.py    # /health endpoint
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings, env vars
│   │   └── exceptions.py    # Custom exceptions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat.py          # Pydantic models for requests/responses
│   │   └── document.py      # Content chunk models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embedding.py     # OpenAI embedding service
│   │   ├── retrieval.py     # Qdrant vector search
│   │   ├── generation.py    # GPT-4o mini answer generation
│   │   ├── citation.py      # Source citation formatting
│   │   └── cache.py         # Caching logic
│   └── db/
│       ├── __init__.py
│       ├── qdrant.py        # Qdrant client
│       └── neon.py          # Neon Postgres (analytics only)
├── scripts/
│   ├── __init__.py
│   ├── index_content.py     # Parse docs, generate embeddings, store
│   └── seed_qdrant.py       # Initial Qdrant collection setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_api.py          # API endpoint tests
│   ├── test_services.py     # Service layer tests
│   └── test_integration.py  # End-to-end pipeline tests
├── pyproject.toml
└── requirements.txt

src/chatbot/                    # Frontend: Docusaurus client module
├── bootstrap.js                # Client module entry point
├── SidebarChatbot.tsx          # Main sidebar component
├── ChatInterface.tsx           # Chat UI (messages, input)
├── useChat.ts                  # React hook for chat state
├── hooks/
│   └── useTextSelection.ts     # Text selection detection hook (US2)
├── services/
│   └── api.ts                  # API client (fetch with retry)
└── types.ts                    # TypeScript interfaces

docs/                            # Textbook content (indexed)
└── [module folders]            # Existing course content
```

---

## Implementation Phases

### Phase 1: Content Indexing

**Goal**: Parse all textbook markdown, generate embeddings, store in Qdrant

**Tasks**:
1. Create Qdrant collection `textbook_chunks` with 1536-dim vectors
2. Implement markdown parser preserving section structure
3. Implement semantic chunking (300-500 tokens, paragraph-aware)
4. Generate embeddings via OpenAI `text-embedding-3-small`
5. Upload chunks to Qdrant with metadata (module, lesson, section, url_anchor)
6. Validate: Search test queries, verify relevant chunks returned

**Acceptance**: All 13 modules indexed, query returns relevant chunks with <0.5s latency

---

### Phase 2: Backend API

**Goal**: FastAPI endpoints for chat with RAG pipeline

**Tasks**:
1. Setup FastAPI app with CORS configuration
2. Implement `/health` endpoint (check Qdrant, OpenAI, Neon connectivity)
3. Implement `/chat` endpoint:
   - Generate embedding for user question
   - Search Qdrant for top 3-5 chunks
   - Generate answer via GPT-4o mini with retrieved context
   - Format citations from chunk metadata
   - Implement browser-local caching (24hr TTL)
4. Implement `/chat/selection` endpoint (text-selection mode)
5. Add error handling (service unavailable, rate limits, no results)
6. Add retry logic (exponential backoff, circuit breaker)
7. Write integration tests

**Acceptance**: `POST /chat` returns cited answers in <2 seconds, handles errors gracefully

---

### Phase 3: Frontend Widget

**Goal**: React sidebar component integrated into Docusaurus

**Tasks**:
1. Create `SidebarChatbot.tsx` component
2. Implement collapsible sidebar (right side, default collapsed)
3. Implement chat interface (message list, input field, send button)
4. Implement loading states and error messages
5. Implement text selection handling:
   - Detect text selection on page
   - Enable "Ask about selection" button
   - Pass selected text to `/chat/selection` endpoint
6. Implement mobile responsive (<768px: full-screen overlay)
7. Add keyboard navigation and ARIA labels (accessibility)
8. Implement browser-local storage for chat history

**Acceptance**: Widget displays on all lesson pages, mobile responsive, keyboard navigable

---

### Phase 4: Integration

**Goal**: Connect frontend to backend, test end-to-end

**Tasks**:
1. Implement API client (`services/api.ts`) with fetch and retry
2. Connect chat widget to `/chat` endpoint
3. Test text selection mode with `/chat/selection`
4. Implement session state (localStorage, sliding window)
5. Test error scenarios (service unavailable, no results)
6. Implement cache fallback (show cached answers during outages)
7. End-to-end testing: User asks question → receives cited answer
8. Performance testing: 50 concurrent users, measure latency

**Acceptance**: User can ask questions and receive answers with citations, <2s response time

---

### Phase 5: Deployment

**Goal**: Deploy to production, validate with real content

**Tasks**:
1. Deploy backend to Railway:
   - Connect GitHub repo
   - Configure environment variables
   - Enable health checks
2. Update frontend `API_URL` for production
3. Run content indexing on production docs
4. Test with production textbook content
5. Monitor: response times, error rates, OpenAI token usage
6. Configure Railway auto-deploys on push to main branch

**Acceptance**: Chatbot functional on GitHub Pages, <2s response time from production URL

---

## Testing Strategy

### Unit Tests
- **Backend**: pytest tests for each service (embedding, retrieval, generation, citation)
- **Frontend**: Jest tests for React components (chat interface, sidebar)

### Integration Tests
- Test full RAG pipeline: question → embedding → retrieval → generation → citation
- Test caching: cache hit, cache miss, cache expiration
- Test error handling: service unavailable, rate limits, empty results

### End-to-End Tests
- User asks question about covered topic → receives answer with citation
- User asks question about uncovered topic → receives "not covered" message
- User selects text and asks question → answer constrained to selection
- Service unavailable during query → cached response shown or retry queued

### Load Tests
- Artillery test: 50 concurrent users, measure p50/p95/p99 latency
- Validate: p95 <2 seconds, no errors

### Accessibility Tests
- Keyboard navigation: Tab through chat interface
- Screen reader: ARIA labels announced correctly
- Color contrast: WCAG AA compliant

---

## Decision Log

| ID | Decision | Rationale | Alternatives Considered |
|----|----------|-----------|------------------------|
| D001 | OpenAI text-embedding-3-small | Low cost ($0.02/1M tokens), multilingual | ada-002 (deprecated), large (5x cost), local (hosting cost) |
| D002 | Markdown-aware semantic chunking | Preserves structure, better retrieval | Fixed char (breaks sentences), sentence-only (too granular) |
| D003 | Browser-local sessions only | Anonymous, private, simple | Server-side (requires auth), hybrid (complex) |
| D004 | 24-hour cache TTL with semantic fallback | High hit rate, content updates propagate | Exact match only (low hit rate), no cache (high cost) |
| D005 | Swizzled Docusaurus theme component | Full control, site-wide injection | Inline (page-specific), iframe (CORS issues) |
| D006 | Standard FastAPI layered structure | Conventional, testable | Single-file (unmaintainable), microservices (overkill) |
| D007 | Railway for backend deployment | Free tier sufficient, easy GitHub integration | Render (similar), Vercel (less suitable for Python) |

---

## Dependencies

### External Services
| Service | Purpose | Tier | Cost |
|---------|---------|------|------|
| Qdrant Cloud | Vector store | Free | $0 |
| OpenAI API | Embeddings + LLM | Pay-per-use | ~$10-50/month estimated |
| Neon Postgres | Analytics logging | Free | $0 |
| Railway | Backend hosting | Free | $0 |

### Python Packages
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
httpx==0.26.0
qdrant-client==1.9.0
openai==1.12.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
tiktoken==0.5.2
pydantic==2.6.0
pytest==8.0.0
pytest-asyncio==0.23.4
```

### NPM Packages
```
react@^18.2.0
@docusaurus/core@^3.0.0
```

---

## Open Questions

| Question | Status | Resolution Plan |
|----------|--------|-----------------|
| Exact chunking algorithm parameters | ✅ Resolved | 300-500 tokens, paragraph-aware (tasks T022-T024) |
| Cache similarity threshold | ✅ Resolved | >0.85 threshold for semantic fallback (task T072) |
| Content re-indexing trigger | Open | Manual for now, webhook in future |

---

## References

- [Research Findings](./research.md) - Technical decisions and alternatives
- [Data Model](./data-model.md) - Entity definitions and relationships
- [API Contract](./contracts/api.yaml) - OpenAPI specification
- [Quickstart Guide](./quickstart.md) - Developer onboarding
- [Feature Specification](./spec.md) - Original requirements and clarifications
