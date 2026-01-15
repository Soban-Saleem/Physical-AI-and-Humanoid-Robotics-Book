---
id: 003
title: rag-chatbot-plan
stage: plan
date: 2025-01-15
surface: claude-code
model: claude-opus-4-5
feature: rag-chatbot
branch: 001-rag-chatbot
user: user
command: /sp.plan
labels: [plan, implementation, rag-chatbot]
links:
  spec: ../../specs/001-rag-chatbot/spec.md
  plan: ../../specs/001-rag-chatbot/plan.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - path: specs/001-rag-chatbot/plan.md
    status: updated
  - path: specs/001-rag-chatbot/research.md
    status: created
  - path: specs/001-rag-chatbot/data-model.md
    status: created
  - path: specs/001-rag-chatbot/quickstart.md
    status: created
  - path: specs/001-rag-chatbot/contracts/api.yaml
    status: created
  - path: CLAUDE.md
    status: updated
tests:
  - name: constitution-check
    status: passed
    coverage: 100%
---

## Prompt

/sp.plan

Create: system architecture diagram, component structure, integration points, data flow.
Decisions needing documentation:
- Vector embedding model selection (OpenAI text-embedding-3-small vs alternatives)
- Chunking implementation strategy (markdown-aware vs naive splitting)
- Session storage approach (browser-only vs hybrid with Neon backup)
- Caching strategy for common questions (TTL, cache key design)
Testing strategy: integration tests for RAG pipeline, E2E tests for chat widget, load testing for 50 concurrent users.

Technical details:
- Use research-concurrent approach (investigate FastAPI + Docusaurus integration patterns while implementing)
- Follow existing codebase patterns (check current Docusaurus config for component registration)
- Organize by phases: Content Indexing → Backend API → Frontend Widget → Integration → Deployment

Phases:
Phase 1 - Content Indexing: Parse markdown files, chunk into 300-500 token paragraphs, generate embeddings, store in Qdrant
Phase 2 - Backend API: FastAPI endpoints for chat, retrieve relevant chunks, generate answers with citations, cache responses
Phase 3 - Frontend Widget: React sidebar component with toggle, mobile responsive, text selection handling
Phase 4 - Integration: Connect widget to backend, error handling, loading states, retry logic
Phase 5 - Deployment: Deploy backend to Railway/Vercel, test with production textbook content

## Response snapshot

Completed `/sp.plan` workflow with all artifacts generated:

**Phase 0: Research** (`research.md`)
- 8 technical decisions documented with rationale and alternatives
- Key decisions: OpenAI text-embedding-3-small, markdown-aware chunking, browser-local sessions, 24hr cache with semantic fallback
- Architecture diagram showing GitHub Pages → Railway → Qdrant/OpenAI/Neon

**Phase 1: Design Artifacts**
- `data-model.md`: 5 entity domains defined (ContentChunk, ChatSession, ChatMessage, CitationReference, CachedResponse) with ERD, validation rules, storage strategy
- `contracts/api.yaml`: OpenAPI 3.0 spec with /chat, /chat/selection, /health endpoints; request/response schemas; error handling
- `quickstart.md`: 15-minute developer onboarding guide with prerequisites, setup steps, common issues

**Plan Update** (`plan.md`)
- Technical Context filled (Python 3.11+, FastAPI, OpenAI, Qdrant, Railway)
- Constitution Check: All applicable principles passed
- Project Structure: Web application (backend + frontend) documented
- 5 Implementation Phases with tasks and acceptance criteria
- Testing Strategy: Unit, Integration, E2E, Load, Accessibility tests defined
- Decision Log: 7 decisions (D001-D007) with rationale

**Agent Context Update**
- CLAUDE.md updated with new technologies: Python 3.11+, TypeScript, FastAPI, OpenAI, Qdrant, Docusaurus
- Enables future AI assistance to understand project tech stack

## Outcome

- ✅ Impact: Complete implementation plan with research-backed technical decisions, ready for task breakdown
- 🧪 Tests: Constitution check passed; testing strategy defined for all quality gates
- 📁 Files: 5 artifacts created (research.md, data-model.md, api.yaml, quickstart.md, plan.md updated)
- 🔁 Next prompts: /sp.tasks to break down into actionable implementation tasks
- 🧠 Reflection: All NEEDS CLARIFICATION items from spec resolved through research phase. Architecture designed for free-tier constraints (Qdrant, Neon, Railway) with 2-second SLA achievable through caching and semantic retrieval.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check - PASS; Technical accuracy - PASS (all decisions verified against official docs)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks for implementation task breakdown
