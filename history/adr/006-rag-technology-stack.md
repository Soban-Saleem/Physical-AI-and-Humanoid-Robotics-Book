# ADR-006: RAG Technology Stack

> **Scope**: AI/ML infrastructure decision cluster for embeddings, LLM, and vector storage.

- **Status:** Accepted
- **Date:** 2025-01-15
- **Feature:** rag-chatbot
- **Context:** Phase 2 - Integrated RAG Chatbot for Physical AI Textbook

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - determines entire AI/ML infrastructure and cost model
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects content indexing, retrieval, answer generation
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use OpenAI for embeddings and generation, with Qdrant Cloud for vector storage.**

**Technology Stack:**
- **Embedding Model:** OpenAI `text-embedding-3-small` (1536 dimensions)
- **Generation Model:** OpenAI GPT-4o mini (cost-effective answer generation)
- **Vector Database:** Qdrant Cloud Free Tier (1 collection, cosine similarity)
- **Retrieval Strategy:** Top 3-5 chunks per query
- **Chunk Size:** 300-500 tokens (semantic paragraph preservation)

**Rationale:**
- Single API key for both embeddings and generation (reduced management overhead)
- `text-embedding-3-small` costs $0.02/1M tokens vs $0.10 for large variant
- Multilingual Training Support (MTS) enables future Urdu translation phase
- Qdrant free tier: 1 collection (sufficient for single textbook)
- GPT-4o mini balances cost and quality for educational Q&A

## Consequences

### Positive

- **Unified API management** - Single OpenAI account for embeddings and generation
- **Cost-effective** - Estimated $10-50/month for expected student traffic
- **Future-proof for Urdu** - `text-embedding-3-small` supports multilingual queries
- **Fast retrieval** - Qdrant Cloud provides <500ms search latency
- **Simple scaling path** - Can upgrade to Qdrant paid tier if needed
- **Mature SDKs** - Both OpenAI and Qdrant have excellent Python/TypeScript support

### Negative

- **Vendor lock-in to OpenAI** - Switching embedding models requires re-indexing all content
- **Rate limits during high traffic** - OpenAI tier limits may affect 50+ concurrent users
- **Qdrant free tier limits** - Single collection constraint (cannot add separate vector stores)
- **Dependent on external service uptime** - Both OpenAI and Qdrant must be available
- **Embedding costs on content updates** - Re-indexing textbook requires new API calls

## Alternatives Considered

### Alternative Stack A: OpenAI Large + Qdrant (Higher Quality)
**Stack:** `text-embedding-3-large` (3072 dims) + GPT-4o mini + Qdrant
**Why rejected:** 5x embedding cost with marginal quality gain for textbook content. Overkill for educational Q&A.

### Alternative Stack B: Sentence Transformers (Local)
**Stack:** Local embedding model (all-MiniLM-L6-v2) + GPT-4o mini + Qdrant
**Why rejected:** Requires hosting infrastructure, slower inference, no cost savings at this scale. Free tier Railway (512MB RAM) insufficient for model hosting.

### Alternative Stack C: OpenAI + Pinecone
**Stack:** `text-embedding-3-small` + GPT-4o mini + Pinecone Free Tier
**Why rejected:** Pinecone free tier limits (1 project, no SIR space) more restrictive than Qdrant. Qdrant has better Python client and documentation.

### Alternative Stack D: Anthropic Claude + Qdrant
**Stack:** Cohere embeddings + Claude Haiku + Qdrant
**Why rejected:** Requires managing multiple API keys. Claude Haiku cheaper but less mature for RAG patterns. Cohere embeddings less widely adopted.

## Migration Path

**If switching embedding models:**
1. Generate new embeddings for all content chunks using new model
2. Create new Qdrant collection or update existing vectors
3. Update backend to use new embedding endpoint
4. No code changes required if vector dimensions match

**If switching vector databases:**
1. Export existing chunks with embeddings
2. Import to new vector database
3. Update backend connection string and client
4. Estimated migration time: 2-4 hours

## References

- Feature Spec: [spec.md](../../specs/001-rag-chatbot/spec.md)
- Implementation Plan: [plan.md](../../specs/001-rag-chatbot/plan.md)
- Research Findings: [research.md](../../specs/001-rag-chatbot/research.md)
- Related ADRs: ADR-001 (Static Site Platform), ADR-005 (Phased Backend Strategy)
