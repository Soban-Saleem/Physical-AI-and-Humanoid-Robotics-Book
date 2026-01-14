# ADR-001: Static Site Platform Architecture

> **Scope**: Infrastructure decision cluster for hosting, deployment, and content delivery platform.

- **Status:** Accepted
- **Date:** 2025-01-13
- **Feature:** textbook-platform
- **Context:** Phase 1 - AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - determines entire deployment model
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects all phases, content delivery, UX
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Deploy Docusaurus 3.9 static site to GitHub Pages for Phase 1 content delivery.**

**Technology Stack:**
- **Static Site Generator:** Docusaurus 3.9
- **Hosting:** GitHub Pages (free tier)
- **CI/CD:** GitHub Actions with official Docusaurus workflow
- **Runtime:** Node.js 20.x LTS (build time only)
- **Deployment Trigger:** Push/merge to `master` branch
- **Content Format:** Markdown with YAML frontmatter (Git versioned)

**Future Integration Points:**
- RAG chatbot backend (FastAPI) - separate deployment
- Authentication (Better Auth) - separate service
- Both will integrate via API calls without migrating existing content

## Consequences

### Positive

- **Zero hosting costs** for Phase 1 - GitHub Pages free tier handles expected traffic
- **AI-powered search** (Docusaurus 3.9 feature) - critical for students navigating 50+ lessons
- **Built-in i18n support** - enables Urdu translation bonus feature without migration
- **Markdown authoring workflow** - content authors use Git + Spec-Kit Plus workflow
- **Fast global CDN** - GitHub Pages Edge network for worldwide student access
- **Version controlled content** - every lesson change tracked in Git history
- **Simple rollback** - revert commit to undo bad deployment
- **No backend maintenance** for Phase 1 - focus on content quality first

### Negative

- **Static-only for Phase 1** - dynamic features (chatbot, progress tracking) require separate backend
- **GitHub Pages limitations** - no server-side code, no database, no WebSocket
- **Build time scaling** - 50+ lessons may approach 10-minute build limit
- **Custom domain requires manual setup** - default is github.io subdomain
- **Plugin ecosystem constraints** - limited to static-compatible plugins

## Alternatives Considered

### Alternative A: Next.js on Vercel
**Stack:** Next.js 14 (App Router) + Vercel hosting
**Why rejected:**
- Over-engineered for content delivery (SSR/ISR not needed)
- Higher complexity for content authors (React components vs Markdown)
- Vercel free tier has bandwidth limits (100GB/month vs GitHub Pages unlimited)
- Better suited for Phase 2 when adding dynamic features

### Alternative B: Hugo on GitHub Pages
**Stack:** Hugo static generator + GitHub Pages
**Why rejected:**
- No AI-powered search (Docusaurus 3.9 has this built-in)
- i18n support weaker for Urdu translation
- Smaller ecosystem for educational site features
- Docusaurus has better documentation and community

### Alternative C: Custom React app with Headless CMS
**Stack:** React + Contentful/Strapi + Vercel
**Why rejected:**
- Adds CMS dependency and cost
- Content authors must learn CMS interface vs Markdown
- Spec-Kit Plus workflow designed for file-based content
- Overkill for Phase 1 launch

### Alternative D: Full-stack from day one (Docusaurus + FastAPI)
**Stack:** Docusaurus frontend + FastAPI backend deployed together
**Why rejected:**
- Slower time to working platform
- Backend infrastructure complexity distracts from content quality
- Can't earn base 100 points until everything works
- Phased approach allows validating content before investing in backend

## Migration Path

**If backend becomes necessary (Phase 2):**
```
Phase 1: Docusaurus on GitHub Pages (current)
     ↓
Phase 2: Add FastAPI on Render/Railway
     ↓
Phase 3: Optional migration to Next.js/Vercel if unified deployment preferred
```

**No content migration required** - Markdown files work with any static site generator.

## References

- Feature Spec: [spec.md](../specs/001-textbook-platform/spec.md)
- Implementation Plan: [plan.md](../specs/001-textbook-platform/plan.md)
- Research: [research.md](../specs/001-textbook-platform/research.md)
- Related ADRs: ADR-005 (Phased Backend Strategy)
