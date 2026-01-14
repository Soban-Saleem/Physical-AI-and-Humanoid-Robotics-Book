# Implementation Plan: AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

**Branch**: `001-textbook-platform` | **Date**: 2025-01-13 | **Spec**: [spec.md](./spec.md)

## Summary

Create an AI-native educational platform teaching Physical AI and Humanoid Robotics using Docusaurus for content delivery, Spec-Kit Plus for spec-driven development, and Claude Code with subagents for content generation. The platform deploys as a static site to GitHub Pages, with plans for integrated RAG chatbot and user authentication in future phases.

**Technical Approach**:
- **Content Platform**: Docusaurus 3.9 with single-instance docs, categorized modules
- **Math Rendering**: KaTeX for performance
- **Code Highlighting**: Palenight (dark) / GitHub (light) themes
- **Diagrams**: Hybrid Mermaid (simple) + external images (complex)
- **Deployment**: GitHub Actions with official Docusaurus workflow
- **Content Creation**: Claude Code subagents (content-implementer, educational-validator)

---

## Technical Context

| Aspect | Decision |
|--------|----------|
| **Language/Version** | JavaScript/TypeScript (Docusaurus 3.9), Node.js 20.x LTS |
| **Primary Dependencies** | Docusaurus 3.9, React 18, KaTeX, Mermaid, Prism |
| **Storage** | Static files (Markdown) + Git version control |
| **Testing** | Educational-validator, factual-verifier subagents |
| **Target Platform** | GitHub Pages (static hosting), responsive web (desktop/tablet/mobile) |
| **Project Type** | Static site generator with spec-driven content creation |
| **Performance Goals** | <2s page load, 10s chatbot response, <3min signup |
| **Constraints** | Static hosting only (no backend for content delivery), mobile-responsive |
| **Scale/Scope** | 6 modules, 50+ lessons, ~50,000 words, 13-week curriculum |

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Spec-Driven Development** | ✅ PASS | All content via `/sp.specify` → `/sp.plan` → `/sp.tasks` → `/sp.implement` |
| **II. Educational Quality** | ✅ PASS | Constitutional checks in educational-validator, framework invisibility enforced |
| **III. Technical Accuracy** | ✅ PASS | Factual-verifier subagent, source verification via WebSearch |
| **IV. Hardware-Awareness** | ✅ PASS | All lessons require hardware requirements + alternatives in frontmatter |
| **V. Subagent Orchestration** | ✅ PASS | Content-implementer mandatory for educational content, direct writing blocked |

**Re-evaluation Post-Design**: All principles maintained. No violations requiring justification.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-platform/
├── spec.md              # User stories, requirements, success criteria
├── plan.md              # This file - technical implementation plan
├── research.md          # Technology research findings (Phase 0 ✅)
├── data-model.md        # Content entities and schema (Phase 1 ✅)
├── quickstart.md        # Getting started guide for authors (Phase 1 ✅)
├── contracts/           # Schema contracts (Phase 1 ✅)
│   ├── lesson-frontmatter-schema.md
│   └── content-structure-schema.md
├── checklists/          # Quality validation checklists
│   └── requirements.md
└── tasks.md             # Task breakdown (Phase 2 - /sp.tasks command)
```

### Source Code (repository root)

```text
physical-ai-robotics-textbook/
├── docs/                     # Docusaurus content
│   ├── intro/                # Front matter (about, prerequisites, hardware guide)
│   ├── module1-intro/        # Weeks 1-2: Introduction to Physical AI
│   ├── module2-ros2/         # Weeks 3-5: ROS 2 Fundamentals
│   ├── module3-simulation/   # Weeks 6-7: Robot Simulation
│   ├── module4-isaac/        # Weeks 8-10: NVIDIA Isaac Platform
│   ├── module5-humanoid/     # Weeks 11-12: Humanoid Development
│   ├── module6-conversational/ # Week 13: Conversational Robotics
│   └── appendices/           # Cheat sheets, troubleshooting, glossary
│
├── .claude/                  # Claude Code configuration
│   ├── agents/               # Educational subagents
│   │   ├── content-implementer.md
│   │   ├── educational-validator.md
│   │   ├── chapter-planner.md
│   │   ├── assessment-architect.md
│   │   └── factual-verifier.md
│   ├── skills/               # Reusable expertise patterns
│   └── commands/             # Spec-Kit Plus slash commands
│
├── .specify/                 # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution.md   # Foundational principles
│   ├── templates/            # Spec, plan, task, ADR templates
│   └── scripts/              # Automation scripts
│
├── specs/                    # Feature specifications
│   └── 001-textbook-platform/
│
├── history/                  # Prompt History Records
│   └── prompts/
│       ├── textbook-platform/
│       └── general/
│
├── blog/                     # Docusaurus blog (announcements, progress)
├── static/                   # Static assets (images, PDFs)
├── src/                      # Docusaurus customizations
│   ├── components/           # React components
│   └── theme/                # Theme overrides
│
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions deployment
│
├── docusaurus.config.js      # Docusaurus configuration
├── sidebars.js               # Navigation structure
├── package.json              # Dependencies
└── CLAUDE.md                 # Project instructions for Claude Code
```

**Structure Decision**: Web application pattern with static site generation. The `docs/` directory contains Markdown content served by Docusaurus. No backend for Phase 1 (content delivery). Backend for RAG chatbot and authentication will be added in future phases.

---

## Architecture Sketch

### Content Creation Workflow

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        CONTENT CREATION                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Author runs /sp.specify                                         │
│     ↓                                                               │
│  2. Spec created: specs/###-feature/spec.md                         │
│     ↓                                                               │
│  3. Author runs /sp.plan                                            │
│     ↓                                                               │
│  4. Plan created: specs/###-feature/plan.md                         │
│     ↓                                                               │
│  5. Author runs /sp.tasks                                           │
│     ↓                                                               │
│  6. Tasks created: specs/###-feature/tasks.md                       │
│     ↓                                                               │
│  7. Author runs /sp.implement                                       │
│     ↓                                                               │
│  8. Content-implementer subagent invoked                            │
│     ├─ Reads 9 skills (blocking)                                   │
│     ├─ Reads reference lesson + constitution                       │
│     ├─ Generates content with YAML frontmatter                     │
│     └─ Writes to docs/module-X/lesson.md                           │
│     ↓                                                               │
│  9. Educational-validator invoked                                   │
│     ├─ Checks framework invisibility                               │
│     ├─ Checks evidence presence                                    │
│     ├─ Checks structural compliance                                │
│     └─ Returns PASS/FAIL with feedback                             │
│     ↓                                                               │
│  10. Factual-verifier invoked (for technical claims)               │
│     ├─ Searches authoritative sources                              │
│     ├─ Validates specifications/versions                           │
│     └─ Flags unverified claims                                     │
│     ↓                                                               │
│  11. PHR created: history/prompts/feature/###-title.phr.md         │
│     ↓                                                               │
│  12. Git commit → PR → Merge → Deploy                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Deployment Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         DEPLOYMENT                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  GitHub Repository (master branch)                                  │
│     │                                                               │
│     ├── push/merge trigger                                         │
│     │                                                               │
│     ▼                                                               │
│  GitHub Actions (.github/workflows/deploy.yml)                      │
│     │                                                               │
│     ├── 1. Checkout code                                            │
│     ├── 2. Setup Node.js 20                                         │
│     ├── 3. Install dependencies (npm ci)                            │
│     ├── 4. Build Docusaurus (npm run build)                         │
│     │                                                               │
│     ▼                                                               │
│  ./build/ directory (static site)                                   │
│     │                                                               │
│     ▼                                                               │
│  GitHub Pages deployment                                            │
│     │                                                               │
│     ▼                                                               │
│  https://YOUR_ORG.github.io/physical-ai-robotics-textbook/         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Site Navigation Structure

```text
Homepage
├── Front Matter
│   ├── About This Course
│   ├── Prerequisites
│   └── Hardware Guide
│
├── Module 1: Introduction to Physical AI (Weeks 1-2)
│   ├── What is Physical AI?
│   ├── Sensors and Actuators
│   └── The Embodiment Gap
│
├── Module 2: ROS 2 Fundamentals (Weeks 3-5)
│   ├── Introduction to ROS 2
│   ├── Nodes and Topics
│   ├── Services and Actions
│   └── URDF and Robot Models
│
├── Module 3: Robot Simulation (Weeks 6-7)
├── Module 4: NVIDIA Isaac Platform (Weeks 8-10)
├── Module 5: Humanoid Development (Weeks 11-12)
├── Module 6: Conversational Robotics (Week 13)
│
└── Appendices
    ├── ROS 2 Cheat Sheet
    ├── Troubleshooting
    ├── Glossary
    └── References
```

---

## Decisions Needing Documentation

### Decision 1: Docusaurus Version

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Docusaurus 3.9 | AI-powered search, i18n support, latest features | Newer, less community documentation | **CHOSEN** |
| Docusaurus 3.x (earlier) | Stable, more examples | Missing AI search features | — |
| Hugo/Jekyll | Faster builds | Less React integration, harder customization | — |

**Rationale**: Docusaurus 3.9's AI-powered search is critical for students navigating large course materials. i18n support enables Urdu translation bonus.

---

### Decision 2: Content Organization

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Single instance with categories | Simple, easy to maintain | Shared versioning | **CHOSEN** |
| Multi-instance docs | Independent versioning per module | More complex, more overhead | — |
| Flat structure | Simplest | Hard to navigate, no module separation | — |

**Rationale**: For initial launch, simplicity is key. Categories provide module separation without multi-instance overhead. Can migrate to multi-instance later if needed.

---

### Decision 3: Math Rendering

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| KaTeX | Fast, small footprint, native Docusaurus support | Fewer advanced features | **CHOSEN** |
| MathJax | More features | Slower, larger, requires custom setup | — |

**Rationale**: KaTeX renders significantly faster and is pre-rendered at build time. Robotics content doesn't require advanced MathJax features.

---

### Decision 4: Code Highlighting Theme

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Palenight/GitHub | Excellent contrast for Python/C++/YAML, standard themes | — | **CHOSEN** |
| Dracula | Popular dark theme | Slightly less contrast for long blocks | — |
| Duotone | Unique look | Lower contrast, harder to read | — |

**Rationale**: Robotics content uses Python, C++, YAML, bash primarily. Palenight excels for these languages and provides excellent readability.

---

### Decision 5: Diagram Approach

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Mermaid only | Text-based, version controlled | Can't handle complex visuals | — |
| External images only | Unlimited complexity | Not version controlled, manual updates | — |
| **Hybrid** | Best of both, appropriate tool per use case | Two systems to maintain | **CHOSEN** |

**Rationale**: Mermaid for architecture/flow diagrams (version controlled), images for complex 3D/screenshots (requires visual fidelity).

---

## Testing Strategy

### Build Tests

```bash
# Local build verification
npm run build
# Expected: Exit code 0, build/ directory created

# Link checking (optional)
npm run build 2>&1 | grep -i "warning\|error"
# Expected: No broken links or missing files
```

### Content Quality Tests

| Check | Method | Criteria |
|-------|--------|----------|
| YAML frontmatter completeness | educational-validator | All required fields present |
| Framework invisibility | educational-validator | No role labels in headers |
| Evidence presence | educational-validator | 70%+ code blocks have Output |
| Structural compliance | educational-validator | Ends with Try With AI |
| Technical accuracy | factual-verifier | All claims verified against sources |
| Spec traceability | grep/spec check | spec_id and requirement_ids valid |

### Deployment Tests

| Check | Method | Criteria |
|-------|--------|----------|
| Site builds | GitHub Actions | Build succeeds |
| Site deploys | GitHub Pages | URL accessible |
| Links work | Manual/automated | All links return 200 |
| Mobile responsive | Browser dev tools | No horizontal scroll on 375px |

### User Acceptance Tests

| Test | Scenario | Expected Result |
|------|----------|-----------------|
| Navigation | Homepage → any lesson | 3 or fewer clicks |
| Page load | Navigate to lesson | <2 seconds on broadband |
| Code display | View code block | Syntax highlighted, scrollable |
| Math rendering | View equation | Renders correctly |
| Try With AI | Complete exercise | Copyable prompt with learning explanation |

---

## Implementation Phases

### Phase 0: Research ✅ COMPLETE

**Status**: All research completed, documented in `research.md`

**Outputs**:
- `research.md` with all technology decisions
- All NEEDS CLARIFICATION items resolved

---

### Phase 1: Design ✅ COMPLETE

**Status**: Design artifacts completed

**Outputs**:
- `data-model.md` - Content entity definitions
- `contracts/lesson-frontmatter-schema.md` - YAML schema
- `contracts/content-structure-schema.md` - Content structure rules
- `quickstart.md` - Getting started guide

---

### Phase 2: Tasks (Next)

**Command**: `/sp.tasks`

**Output**: `tasks.md` with ordered task breakdown

---

### Phase 3: Implementation

**Command**: `/sp.implement`

**Tasks**:
1. Initialize Docusaurus site structure
2. Configure KaTeX, Mermaid, code highlighting
3. Create navigation (sidebars.js)
4. Write front matter content (intro, prerequisites, hardware guide)
5. Implement Module 1 lessons (4 lessons minimum)
6. Configure GitHub Actions deployment
7. Test build and deployment
8. Create appendices

---

## Quality Gates

### Before Publication

- [ ] All lessons have complete YAML frontmatter
- [ ] All lessons pass educational-validator
- [ ] All technical claims verified
- [ ] Hardware requirements specified
- [ ] Simulation alternatives provided
- [ ] Site builds locally without errors
- [ ] Mobile responsive design verified

### Before Deployment

- [ ] All links resolve
- [ ] No broken images
- [ ] Math equations render
- [ ] Code blocks highlighted
- [ ] GitHub Actions workflow configured

---

## References

- **Research**: `research.md`
- **Data Model**: `data-model.md`
- **Contracts**: `contracts/`
- **Quickstart**: `quickstart.md`
- **Constitution**: `.specify/memory/constitution.md`
- **Spec**: `spec.md`

---

**Plan Status**: COMPLETE | Ready for `/sp.tasks` command
