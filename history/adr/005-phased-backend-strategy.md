# ADR-005: Phased Backend Strategy

> **Scope**: Timeline for implementing dynamic features (RAG chatbot, authentication) that require backend infrastructure.

- **Status:** Accepted
- **Date:** 2025-01-13
- **Feature:** textbook-platform
- **Context:** Spec includes P2 (RAG chatbot) and P3 (authentication) features requiring backend, but hackathon prioritizes base functionality (static content delivery)

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - determines when/how backend integrates
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 3 phased approaches evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects deployment, costs, student experience
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Phase 1: Static content delivery only. Backend for chatbot and authentication deferred to Phase 2.**

**Phase Breakdown:**

| Phase | Focus | Features | Hosting | Hackathon Points |
|-------|-------|----------|---------|------------------|
| **Phase 1** (Current) | Content delivery | Docusaurus site, 50+ lessons, YAML frontmatter, subagents | GitHub Pages (free) | 100 (base) |
| **Phase 2** (Future) | Interactive features | RAG chatbot, user authentication, progress tracking | Render/Railway/Fly | +100 (bonus) |

**Phase 2 Backend Stack (to be implemented):**
- **API Framework:** FastAPI (Python)
- **Vector Database:** Qdrant Cloud (free tier: 1GB)
- **LLM:** OpenAI API (GPT-4 for responses, embeddings for search)
- **User Database:** Neon Postgres (serverless PostgreSQL)
- **Authentication:** Better Auth (OIDC, PKCE flows)
- **CORS:** Configured for Docusaurus origin

## Consequences

### Positive

- **Faster time to working platform** - focus on content quality first
- **Lower initial complexity** - no backend debugging during content creation
- **Clear hackathon priorities** - base 100 points achievable without backend
- **Backend decisions informed by real content** - chatbot trained on actual lessons
- **Separation of concerns** - content authors work independently of backend developers
- **Incremental cost scaling** - only pay for backend when needed

### Negative

- **No AI chatbot in Phase 1** - students can't ask questions about content
- **No progress tracking** - can't save lesson completion or resume position
- **No user accounts** - can't personalize by technical background
- **Future integration work** - must add API endpoints, CORS, authentication later
- **Potential for disjointed UX** - static site + separate backend may feel less integrated

## Migration Path

**Phase 1 → Phase 2 Integration:**

```
Phase 1:
┌─────────────────────────────────────┐
│  Docusaurus on GitHub Pages         │
│  - Static content only              │
│  - No backend calls                 │
└─────────────────────────────────────┘

Phase 2:
┌─────────────────────────────────────┐
│  Docusaurus on GitHub Pages         │
│  - Chat widget API calls →          │
│  - Login redirects to →             │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  FastAPI Backend (Render/Railway)   │
│  - /api/chat (RAG + OpenAI)         │
│  - /api/auth/* (Better Auth)        │
│  - Qdrant (vector search)           │
│  - Neon Postgres (users, progress)  │
└─────────────────────────────────────┘
```

**Integration Steps:**
1. Deploy FastAPI backend with `/api/chat` endpoint
2. Add chat widget to Docusaurus (fetch from backend API)
3. Configure CORS for GitHub Pages origin
4. Add Better Auth with OAuth/OIDC providers
5. Add progress tracking API endpoints
6. Deploy user database migrations

**No content migration required** - existing Markdown lessons work with both phases.

## Alternatives Considered

### Alternative A: Build Everything in Phase 1
**Approach:** Implement chatbot and authentication alongside static site from day one
**Why rejected:**
- Significantly slower time to working platform
- Backend debugging distracts from content quality
- Can't earn base 100 points until everything works
- Higher initial complexity increases failure risk
- **Hackathon strategy:** Deliver base functionality first, add bonuses if time permits

### Alternative B: Backend-First Architecture
**Approach:** Build FastAPI backend first, then add Docusaurus frontend
**Why rejected:**
- Content authors need platform working to generate lessons
- Backend without content is useless (no RAG without documents to index)
- Can't test chatbot quality without real lesson content
- **Content is king:** Educational platform value is in the lessons

### Alternative C: Monolithic Deployment (Docusaurus + Backend Together)
**Approach:** Deploy Docusaurus and FastAPI as single unit (e.g., Docker container on Railway)
**Why rejected:**
- Loses GitHub Pages free tier advantage
- More complex deployment (Docker vs static file hosting)
- Slower builds (must build backend + frontend together)
- Harder rollback (backend + frontend coupled)
- **Separation of concerns:** Static content rarely changes; backend will iterate on chatbot quality

## Bonus Feature Dependencies

| Bonus Feature | Points | Backend Dependencies | Phase |
|---------------|--------|---------------------|-------|
| Claude Code subagents/skills | +50 | None (content authoring only) | Phase 1 |
| Better Auth (signup/signin) | +50 | FastAPI + Neon Postgres + Better Auth | Phase 2 |
| Content personalization | +50 | User database + recommendation logic | Phase 2 |
| Urdu translation | +50 | Docusaurus i18n (no backend needed) | Phase 2+ |

**Note:** Claude Code subagents/skills (+50) achievable in Phase 1 as content authoring infrastructure, not runtime feature.

## Cost Implications

| Phase | Hosting | Monthly Cost (USD) |
|-------|---------|-------------------|
| **Phase 1** | GitHub Pages | $0 |
| **Phase 2** | GitHub Pages + Render (Free tier) + Qdrant Cloud (Free) + Neon (Free) | $0 - $20* |

*Phase 2 costs only if free tiers exhausted (high traffic, large vector database).

**Phase 2 Paid Tier Triggers:**
- Qdrant: >1GB vector storage (~50k pages of text)
- Render/Railway: >750 hours/month (always-on backend required)
- Neon: >3 GB database or >300 Active Row hours

## Student Experience Impact

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| Content access | ✅ Full | ✅ Full |
| Search (content) | ✅ AI-powered | ✅ AI-powered |
| Ask AI questions | ❌ Not available | ✅ RAG chatbot |
| Save progress | ❌ Not available | ✅ Account required |
| Personalization | ❌ Not available | ✅ Background-based |
| Mobile responsive | ✅ Yes | ✅ Yes |

## Risk Mitigation

**Risk:** Students expect interactive features from launch

**Mitigation:**
- Clear communication that Phase 1 is content-focused
- "Coming soon" indicators for chatbot/auth features
- Focus on content quality as primary value proposition
- Gather feedback on content before adding interactive features

**Risk:** Phase 2 backend integration breaks Phase 1 content

**Mitigation:**
- Content is static Markdown - no backend dependencies
- API calls are additive - existing content unaffected
- Test Phase 2 in staging environment before production
- Keep Phase 1 GitHub Pages deployment as fallback

## References

- Feature Spec: [spec.md](../specs/001-textbook-platform/spec.md) - User Stories 2 (P2) and 3 (P3)
- Implementation Plan: [plan.md](../specs/001-textbook-platform/plan.md)
- Research: [research.md](../specs/001-textbook-platform/research.md)
- Related ADRs: ADR-001 (Static Site Platform)
