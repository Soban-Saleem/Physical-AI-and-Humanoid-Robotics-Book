# ADR-009: Docusaurus Chatbot Integration Pattern

> **Scope**: Frontend integration decision cluster for embedding chatbot widget into Docusaurus site.

- **Status:** Accepted
- **Date:** 2025-01-15
- **Feature:** rag-chatbot
- **Context:** Phase 2 - Integrated RAG Chatbot for Physical AI Textbook

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - determines how frontend is built and maintained
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects all lesson pages and site navigation
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use swizzled Docusaurus theme component with client modules for React sidebar injection.**

**Integration Strategy:**
- **Method:** Swizzle Docusaurus theme + clientModules registration
- **Component:** Collapsible right sidebar (default collapsed, expands on toggle)
- **Mobile Behavior:** Full-screen overlay below 768px width
- **State Management:** React Context for chat state across navigation
- **Text Selection:** Window Selection API for "Ask about selection" feature

**Implementation Points:**

**1. docusaurus.config.js** - Register client module:
```javascript
export default {
  clientModules: [require.resolve('./src/chatbot/bootstrap.js')],
};
```

**2. src/chatbot/bootstrap.js** - Entry point for widget initialization

**3. src/chatbot/SidebarChatbot.tsx** - Main React component

**4. Text Selection Handling** - Use `window.getSelection()` API

## Consequences

### Positive

- **Site-wide availability** - Widget appears on all lesson pages without manual insertion
- **Consistent UX** - Single sidebar component across entire textbook
- **State persists across navigation** - React Context maintains chat history
- **Text selection access** - Can access page content for "Ask about selection" feature
- **No iframe restrictions** - Full DOM access for citations and navigation
- **Mobile responsive** - Full-screen overlay pattern for small screens

### Negative

- **Swizzle maintenance** - Docusaurus theme updates require manual merge
- **Client module complexity** - Adds build-time initialization logic
- **React Context global state** - Potential state management complexity at scale
- **Load on all pages** - Widget JavaScript loads even when not used

## Alternatives Considered

### Alternative A: Inline Component Per Page
**Strategy:** Import chatbot component in each markdown lesson
**Why rejected:** Requires updating 50+ lesson files, inconsistent placement, no text selection access. Not site-wide.

### Alternative B: iframe/External Widget
**Strategy:** Embed chatbot as iframe from separate origin
**Why rejected:** CORS blocks text selection access, iframe isolation prevents citations linking, poor UX.

### Alternative C: Browser Extension
**Strategy:** Chrome/Firefox extension for chatbot
**Why rejected:** Installation friction (students must install), no guaranteed adoption, harder to maintain. Violates "embedded" requirement.

### Alternative D: Third-Party Chat Widget
**Strategy:** Use Intercom, Crisp, or similar widget
**Why rejected:** Doesn't integrate with our RAG backend, monthly cost, generic UI not tailored for education.

## Migration Path

**If swizzling becomes problematic:**
1. Evaluate Docusaurus 4.x native injection methods
2. Consider migrating to inline component with automated script (adds to all markdown files)
3. Worst case: Build custom Docusaurus theme (full control, full maintenance burden)

**If React Context proves insufficient:**
1. Add state management library (Zustand, Jotai) for complex chat scenarios
2. Migrate Context to Zustand with minimal component changes
3. Estimated migration time: 2-4 hours

## References

- Feature Spec: [spec.md](../../specs/001-rag-chatbot/spec.md)
- Implementation Plan: [plan.md](../../specs/001-rag-chatbot/plan.md)
- Research Findings: [research.md](../../specs/001-rag-chatbot/research.md)
- Related ADRs: ADR-001 (Static Site Platform)
