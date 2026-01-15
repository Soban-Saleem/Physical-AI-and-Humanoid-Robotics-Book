# ADR-007: Content Chunking Strategy for RAG

> **Scope**: Content processing decision cluster for how textbook content is prepared for vector retrieval.

- **Status:** Accepted
- **Date:** 2025-01-15
- **Feature:** rag-chatbot
- **Context:** Phase 2 - Integrated RAG Chatbot for Physical AI Textbook

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - determines retrieval quality and answer accuracy
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects content indexing pipeline and RAG pipeline
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use markdown-aware semantic chunking with paragraph preservation, targeting 300-500 tokens per chunk.**

**Chunking Strategy:**
- **Parser:** Markdown AST parser (markdown-it or similar)
- **Chunk Size:** 300-500 tokens (target 400, midpoint of range)
- **Boundary Preference:** Paragraph breaks > sentence breaks > forced
- **Code Blocks:** Never split (teaching units must stay intact)
- **Metadata:** Include section path (module > lesson > section) in each chunk
- **Token Counter:** tiktoken with cl100k_base encoding

**Implementation Logic:**
```python
1. Parse markdown to AST
2. Traverse AST tracking:
   - Current section path (e.g., "Module 1 > Sensors > LIDAR")
   - Accumulated token count
   - Code block boundaries
3. Create chunks:
   - Prefer paragraph boundaries
   - Never split code blocks
   - Include section context in metadata
   - Target 400 tokens (300-500 range)
```

## Consequences

### Positive

- **Preserves semantic meaning** - Paragraph-level boundaries maintain conceptual coherence
- **Better retrieval quality** - Section headers provide valuable context for vector search
- **Code examples remain intact** - Teaching units not broken across chunks
- **Consistent chunk sizes** - 300-500 token range ensures uniform embedding quality
- **Reproducible** - Deterministic chunking allows re-indexing without drift

### Negative

- **More complex than fixed-size** - Requires AST parsing vs simple character counting
- **Slower indexing** - Markdown parsing adds overhead to content pipeline
- **Tuning required** - Optimal token boundaries may need adjustment based on content
- **Code blocks may exceed targets** - Large code examples could create oversized chunks

## Alternatives Considered

### Alternative A: Fixed Character Chunks
**Strategy:** Split content every 1000 characters regardless of structure
**Why rejected:** Breaks sentences mid-word, loses paragraph context, poor retrieval quality. Students receive fragmented answers.

### Alternative B: Sentence-Level Chunks
**Strategy:** Chunk every 2-3 sentences
**Why rejected:** Too granular, creates 10,000+ chunks, slower retrieval, loses paragraph coherence.

### Alternative C: Section-Based Chunks
**Strategy:** Each markdown ## section becomes one chunk
**Why rejected:** Variable sizes (some sections too large for context window), may exceed 500 tokens significantly, requires splitting anyway.

### Alternative D: Recursive Character Splitting
**Strategy:** LangChain's RecursiveCharacterTextSplitter with overlapping chunks
**Why rejected:** Overlap confuses citation generation, doesn't respect markdown structure, LangChain dependency overhead.

## Migration Path

**If chunking strategy needs adjustment:**
1. Update chunking logic in `scripts/index_content.py`
2. Re-run indexing pipeline (clear Qdrant collection, re-upload)
3. No backend code changes if metadata structure preserved
4. Estimated re-indexing time: 10-30 minutes depending on content size

**Tuning parameters (no full re-index):**
- Token range (300-500) can be adjusted without changing logic
- Section metadata format changes require re-indexing

## References

- Feature Spec: [spec.md](../../specs/001-rag-chatbot/spec.md)
- Implementation Plan: [plan.md](../../specs/001-rag-chatbot/plan.md)
- Research Findings: [research.md](../../specs/001-rag-chatbot/research.md)
- Data Model: [data-model.md](../../specs/001-rag-chatbot/data-model.md)
- Related ADRs: ADR-006 (RAG Technology Stack)
