---
id: 001
title: rag-chatbot-spec
stage: spec
date: 2025-01-15
surface: claude-code
model: claude-opus-4-5
feature: rag-chatbot
branch: 001-rag-chatbot
user: user
command: /sp.specify
labels: [spec, rag-chatbot, phase-2]
links:
  spec: ../../specs/001-rag-chatbot/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - path: specs/001-rag-chatbot/spec.md
    status: created
  - path: specs/001-rag-chatbot/checklists/requirements.md
    status: created
tests:
  - name: requirements-checklist
    status: passed
    coverage: 100%
---

## Prompt

/sp.specify Integrated RAG Chatbot for Physical AI Textbook Platform

Target audience: Students and professionals learning Physical AI & Humanoid Robotics
Focus: Contextual Q&A about book content with text-selection-aware responses

Success criteria:
- Chatbot widget embedded in Docusaurus book pages (right sidebar or floating)
- RAG pipeline indexes all 13 modules of markdown course content
- Answers questions about book content with source citations (lesson + section)
- "Ask about selection" feature: user highlights text → chatbot answers only based on selection
- FastAPI backend serves chat endpoints with <2s response time
- Qdrant Cloud vector store with semantic search on course content
- Neon Serverless Postgres stores chat history and user sessions
- OpenAI GPT-4o mini for answer generation (cost-effective)

Technical Configuration:
- Qdrant URL: <configured via QDRANT_URL env var>
- Qdrant API Key: <configured via QDRANT_API_KEY env var>
- Qdrant Cluster ID: <your-cluster-id>
- Neon DB URL: <configured via NEON_DATABASE_URL env var>
- OpenAI API Key: <configured via OPENAI_API_KEY env var>

Constraints:
- Tech stack: FastAPI (backend), Docusaurus React (frontend), Qdrant Cloud (vectors), Neon Postgres (data), OpenAI API (LLM)
- Deployment: Vercel/Railway for backend, existing GitHub Pages for frontend
- Budget: Free tiers only (Qdrant Free, Neon Free Tier), OpenAI API usage monitored
- Latency: First answer <2 seconds, subsequent turns <1 second
- Offline mode: Graceful fallback when API unavailable
- Timeline: Phase 2 complete before hackathon deadline (Nov 30, 2025)

Not building:
- General-purpose chatbot (answers only from textbook content, not web)
- User authentication for chat (anonymous sessions with browser storage)
- Admin dashboard for viewing user conversations
- Multi-language support (Urdu translation is separate Phase 3)
- Real-time collaboration features
- Voice input/output (reserved for Module 13 - Conversational Robotics)

## Response snapshot

Created specification file at `specs/001-rag-chatbot/spec.md` with the following structure:

1. **Overview**: Intelligent Q&A assistant embedded in the textbook platform
2. **Scope Boundaries**: Defined in-scope (textbook-only Q&A, text-selection mode, citations) and out-of-scope (web search, auth, admin dashboard, multi-language, voice)
3. **User Stories**: 3 prioritized independently testable stories:
   - P1: Ask Questions About Course Content (core Q&A with citations)
   - P2: Text-Selection-Aware Q&A (focused answers on highlighted text)
   - P3: Conversation Context Memory (follow-up question handling)
4. **Edge Cases**: 7 scenarios covered including no results, service unavailable, large selections, non-English questions, concurrent users, page navigation, content updates
5. **Functional Requirements**: 15 testable requirements (FR-001 through FR-015)
6. **Non-Functional Requirements**: Performance, availability, privacy, accessibility, browser support
7. **Key Entities**: Chat Message, Chat Session, Content Chunk, Citation Reference
8. **Success Criteria**: 7 measurable outcomes (SC-001 through SC-007)
9. **Dependencies & Assumptions**: External services and content assumptions documented
10. **Technical Configuration Notes**: Implementation reference section (kept separate from technology-agnostic requirements)

Created requirements checklist at `specs/001-rag-chatbot/checklists/requirements.md` - all items passed.

## Outcome

- ✅ Impact: Complete specification for Phase 2 RAG Chatbot ready for implementation planning
- 🧪 Tests: Requirements checklist passed 100% - no clarifications needed, all items testable and technology-agnostic
- 📁 Files: spec.md (created), checklists/requirements.md (created)
- 🔁 Next prompts: /sp.plan to create implementation plan, /sp.clarify if questions arise
- 🧠 Reflection: User provided comprehensive requirements including credentials and clear scope boundaries. No [NEEDS CLARIFICATION] markers needed as all requirements were specific enough to make informed decisions.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Requirements checklist - PASS (14/14 items)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.plan to break down implementation tasks
