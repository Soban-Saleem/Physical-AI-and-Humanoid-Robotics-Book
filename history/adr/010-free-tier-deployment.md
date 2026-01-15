# ADR-010: Free-Tier Deployment Architecture

> **Scope**: Infrastructure decision cluster for backend hosting and services within cost constraints.

- **Status:** Accepted
- **Date:** 2025-01-15
- **Feature:** rag-chatbot
- **Context:** Phase 2 - Integrated RAG Chatbot for Physical AI Textbook

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - determines hosting costs, scaling limits, and reliability
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects all external services and deployment pipeline
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Deploy backend on Railway free tier with Qdrant Cloud and Neon Postgres free tiers for vector storage and analytics.**

**Deployment Architecture:**
- **Backend Hosting:** Railway Free Tier (512MB RAM, 0.5 CPU, 500hrs/month)
- **Vector Storage:** Qdrant Cloud Free Tier (1 collection, 1GB vector storage)
- **Analytics DB:** Neon Postgres Free Tier (3 active DBs, 97.28GB storage)
- **Frontend:** Existing GitHub Pages (no additional cost)
- **CI/CD:** Railway auto-deploy on push to main branch

**Infrastructure Diagram:**
```
GitHub Pages (Frontend)
    ↓ HTTPS
Railway (FastAPI Backend)
    ├─→ Qdrant Cloud (Vectors)
    ├─→ OpenAI API (Embeddings + LLM)
    └─→ Neon Postgres (Analytics)
```

**Environment Variables (Railway):**
```bash
QDRANT_URL=***
QDRANT_API_KEY=***
OPENAI_API_KEY=***
NEON_DATABASE_URL=***
CORS_ORIGINS=https://soban-saleem.github.io
```

**Free Tier Constraints:**
- Railway: 512MB RAM, 0.5 CPU, sleeps after 15min inactivity
- Qdrant: 1 collection, 1GB storage (sufficient for ~3M vectors)
- Neon: 3 active databases, 97GB storage (analytics only)

## Consequences

### Positive

- **Zero hosting costs** - All infrastructure on free tiers
- **GitHub integration** - Railway auto-deploys on push
- **Simple scaling path** - Can upgrade to paid tiers when needed
- **Environment variable security** - API keys not committed to git
- **Graceful degradation** - Cached responses work during Railway sleep

### Negative

- **Railway cold starts** - 15min sleep means first request after inactivity wakes service (~10s delay)
- **Single Qdrant collection** - Cannot add separate vector stores without paid tier
- **Free tier limits** - 50 concurrent users near Railway capacity, may need upgrade
- **No vertical scaling** - Cannot increase RAM/CPU without paying
- **Vendor lock-in** - Migrating from Railway requires redeployment

## Alternatives Considered

### Alternative A: Render Free Tier
**Stack:** Render free tier (512MB RAM, 750hrs/month) + Qdrant + Neon
**Why rejected:** Similar constraints to Railway, less integrated GitHub experience. Railway's auto-deploy superior.

### Alternative B: Vercel Serverless
**Stack:** Vercel Functions + Qdrant + Neon
**Why rejected:** Vercel less suitable for Python FastAPI, cold starts on every request, 10s execution limit problematic for RAG pipeline.

### Alternative C: Self-Hosted on VPS
**Stack:** DigitalOcean droplet ($6-24/month) + self-hosted Qdrant + Postgres
**Why rejected:** Adds monthly cost, requires server maintenance, negates free-tier advantage. Only justified if free tiers exhausted.

### Alternative D: Cloudflare Workers + KV
**Stack:** Cloudflare Workers (Python beta) + Workers KV + D1
**Why rejected:** Workers KV not suitable for vector similarity search, D1 not mature for production, edge execution adds latency to database calls.

## Migration Path

**If Railway free tier insufficient:**
1. Upgrade to Railway Hobby plan ($5/month): 512MB RAM, always-on
2. Or migrate to Render Standard ($7/month): 2GB RAM, better performance
3. No code changes required - only platform and environment variable migration

**If Qdrant free tier exhausted:**
1. Upgrade to Qdrant Cloud Starter ($25/month): 10 collections, 10GB storage
2. Or migrate to Pinecone (similar pricing)
3. Requires re-indexing content if switching vector databases

**If Neon free tier exhausted:**
1. Upgrade to Neon Pro ($19/month): 3 active DBs, 100GB storage
2. Or migrate to Supabase free tier (similar constraints)
3. Analytics is non-critical - can disable if needed

## Acceptance Criteria

**Free tier sufficient when:**
- < 50 concurrent students using chatbot simultaneously
- < 3,000 content chunks (~13 modules of textbook)
- < 10,000 questions per month
- Railway cold start delay acceptable (~10s first request after inactivity)

**Trigger paid upgrade when:**
- Consistent 50+ concurrent users
- Qdrant storage approaching 1GB
- Need for additional vector collections
- Railway sleep causing user complaints

## References

- Feature Spec: [spec.md](../../specs/001-rag-chatbot/spec.md)
- Implementation Plan: [plan.md](../../specs/001-rag-chatbot/plan.md)
- Research Findings: [research.md](../../specs/001-rag-chatbot/research.md)
- Related ADRs: ADR-001 (Static Site Platform), ADR-005 (Phased Backend Strategy), ADR-006 (RAG Technology Stack)
