# ADR-008: Browser-Local Session and Cache Architecture

> **Scope**: Client-side data management decision cluster for session state and response caching.

- **Status:** Accepted
- **Date:** 2025-01-15
- **Feature:** rag-chatbot
- **Context:** Phase 2 - Integrated RAG Chatbot for Physical AI Textbook

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - determines privacy model, UX, and cost structure
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects frontend widget, backend API, and user privacy
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use browser-local storage for all session state and response caching, with 24-hour TTL and semantic similarity fallback.**

**Storage Architecture:**
- **Session State:** localStorage (UUID, message history, context window)
- **Response Cache:** IndexedDB (question hash → answer with citations)
- **TTL:** 24 hours (content updates propagate daily)
- **Cache Strategy:** Exact match + semantic similarity fallback (>0.85)
- **Session Scope:** Anonymous, per-browser, no cross-device sync

**Storage Schema:**

```typescript
// localStorage - ChatSession
interface ChatSession {
  sessionId: string;        // UUID v4
  startTime: number;        // Unix timestamp
  messages: ChatMessage[];  // Max 50 for context
  contextWindow: string[];  // Last 10 message IDs (sliding)
}

// IndexedDB - CachedResponse
interface CachedResponse {
  cacheKey: string;         // SHA-256 hash
  answer: string;
  citations: CitationReference[];
  createdAt: number;
  ttl: 86400000;            // 24 hours
  hitCount: number;
}
```

**Server-Side (Neon Postgres):**
- Used ONLY for anonymized analytics (interaction_log table)
- No session state stored server-side
- No PII or user-identifiable information

## Consequences

### Positive

- **Privacy-first** - No user data leaves the browser except anonymized analytics
- **Zero auth infrastructure** - Anonymous sessions meet spec requirements
- **Fast responses** - Cache hits return instantly (<100ms)
- **High cache hit rate** - Semantic fallback captures paraphrased questions
- **Simple backend** - No session management complexity
- **GDPR compliant** - No personal data stored on servers

### Negative

- **No cross-device continuity** - Students lose history when switching devices
- **Cache cleared on browser clear** - Users lose all cached responses
- **Limited context window** - 50-message localStorage constraint
- **No conversation analytics** - Cannot analyze student learning patterns beyond anonymized logs
- **IndexedDB complexity** - More complex than localStorage for cache

## Alternatives Considered

### Alternative A: Server-Side Sessions
**Strategy:** Store all sessions in Neon Postgres with session ID cookies
**Why rejected:** Requires authentication infrastructure, violates privacy-first approach, adds backend complexity. Spec explicitly requires anonymous sessions.

### Alternative B: Hybrid with Cloud Backup
**Strategy:** localStorage + Neon backup for cross-device sync
**Why rejected:** Requires session ID management, adds complexity, still needs auth for cross-device. Out of scope for MVP.

### Alternative C: Exact Match Cache Only
**Strategy:** Cache only on exact question string match
**Why rejected:** Lower hit rate, misses paraphrased questions. Students often ask same question differently.

### Alternative D: No Caching
**Strategy:** Every question hits OpenAI API
**Why rejected:** Higher costs ($50-100/month vs $10-50), slower responses, violates 2-second SLA during API rate limits.

## Migration Path

**If server-side sessions become necessary (future feature):**
1. Add authentication layer (Better Auth, as planned for other features)
2. Migrate localStorage format to match Neon session schema
3. Add session sync endpoint to backend
4. Frontend: Implement sync logic with conflict resolution

**If cache strategy needs adjustment:**
- TTL can be changed without migration (just update constant)
- Similarity threshold (0.85) can be tuned based on hit rate metrics
- Cache key format changes invalidate existing cache (acceptable, user-transparent)

## References

- Feature Spec: [spec.md](../../specs/001-rag-chatbot/spec.md)
- Implementation Plan: [plan.md](../../specs/001-rag-chatbot/plan.md)
- Research Findings: [research.md](../../specs/001-rag-chatbot/research.md)
- Data Model: [data-model.md](../../specs/001-rag-chatbot/data-model.md)
- Related ADRs: ADR-006 (RAG Technology Stack)
