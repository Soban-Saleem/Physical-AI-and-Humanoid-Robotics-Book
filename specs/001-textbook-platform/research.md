# Research: AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

**Feature**: `001-textbook-platform` | **Phase**: 0 (Research) | **Date**: 2025-01-13

## Overview

This document consolidates technology research findings for implementing an AI-native educational platform using Docusaurus, Spec-Kit Plus, and Claude Code. Research addresses all technical decisions needed for implementation.

---

## 1. Docusaurus Configuration

### Decision: Docusaurus 3.9

**Rationale**: Docusaurus 3.9 (October 2025) includes AI-powered search for enhanced content discoverability - critical for students navigating large course materials.

**Key Features**:
- AI-powered search (new in 3.9)
- Enhanced multi-language support (i18n) for Urdu translation bonus
- MDX support for interactive components
- Native KaTeX integration for math rendering

**Alternatives Considered**:
- Docusaurus 3.x (earlier versions) - lacks AI search features
- Hugo/Jekyll - less integrated with React ecosystem
- Next.js - requires more custom configuration for doc sites

**Sources**:
- [Docusaurus 3.9 Release Notes](https://docusaurus.io/blog/releases/3.0)
- [InfoQ: Docusaurus 3.9 AI Search](https://www.infoq.com/news/2025/10/docusaurus-3-9-ai-search/)

---

## 2. Content Organization: Single Instance with Categories

### Decision: Single Docusaurus docs instance with categorized modules

**Rationale**: Simpler to implement and maintain than multi-instance for initial launch. Categories provide module separation without complexity overhead.

**Directory Structure**:
```text
docs/
├── intro/                 # Module 0: Front matter
│   ├── about.md
│   ├── prerequisites.md
│   └── hardware-guide.md
├── module1-intro/         # Weeks 1-2: Introduction to Physical AI
├── module2-ros2/          # Weeks 3-5: ROS 2 Fundamentals
├── module3-simulation/    # Weeks 6-7: Robot Simulation
├── module4-isaac/         # Weeks 8-10: NVIDIA Isaac Platform
├── module5-humanoid/      # Weeks 11-12: Humanoid Development
├── module6-conversational/ # Week 13: Conversational Robotics
└── appendices/
    ├── ros2-cheat-sheet.md
    ├── troubleshooting.md
    ├── glossary.md
    └── references.md
```

**Alternatives Considered**:
- Multi-instance docs - allows independent versioning per module, but adds overhead
- Flat structure - no module separation, harder to navigate

**Sources**:
- [Docusaurus Docs Multi-Instance](https://docusaurus.io/docs/docs-multi-instance)
- [Courseasaurus Document Collections](https://github.com/neu-pdi/courseasaurus)

---

## 3. Math Rendering: KaTeX

### Decision: Use KaTeX for equation rendering

**Rationale**:
- Significantly faster rendering than MathJax
- Smaller library footprint (~150KB vs ~500KB+)
- Native Docusaurus support via remark plugin
- Pre-rendered at build time (static site friendly)

**Configuration**:
```javascript
remarkPlugins: [require('@docusaurus/remark-plugin-katex')]
```

**When MathJax Would Be Needed**:
- Advanced mathematical features not supported by KaTeX (rare for robotics content)

**Sources**:
- [Docusaurus Math Equations](https://docusaurus.io/docs/markdown-features/math-equations)
- [KaTeX vs MathJax Discussion](https://meta.mathoverflow.net/questions/1908/katex-vs-mathjax)

---

## 4. Code Highlighting: Palenight (Dark) / GitHub (Light)

### Decision: Use Palenight for dark mode, GitHub for light mode

**Rationale**: Both themes provide excellent contrast for Python, C++, YAML, and bash - the primary languages in robotics education.

**Languages to Support**:
- `python` (built-in) - ROS 2 Python nodes
- `bash` (built-in) - Terminal commands
- `cpp` (built-in) - ROS 2 C++ nodes
- `yaml` (built-in) - Robot descriptions, configs
- `xml` (built-in) - URDF files

**Configuration**:
```javascript
const prismThemes = require('prism-react-renderer/themes');

themeConfig: {
  prism: {
    theme: prismThemes.github,
    darkTheme: prismThemes.palenight,
    additionalLanguages: ['bash', 'cpp', 'yaml', 'xml'],
  },
}
```

**Alternatives Considered**:
- Dracula - popular dark theme, good alternative
- Duotone - less contrast for long code blocks

**Sources**:
- [Docusaurus Code Blocks](https://docusaurus.io/docs/markdown-features/code-blocks)

---

## 5. Diagrams: Hybrid (Mermaid + External Images)

### Decision: Use Mermaid for simple diagrams, external images for complex visualizations

**Mermaid For**:
- Flowcharts (algorithm flows, control systems)
- Sequence diagrams (ROS 2 node communication)
- State diagrams (robot state machines)
- Architecture diagrams (system components)

**External Images For**:
- Complex 3D robot kinematics
- Sensor data visualizations
- Screenshots from Gazebo/Isaac Sim
- Photographs of physical hardware

**Rationale**: Mermaid is text-based (version controlled), themes automatically, but can't handle complex visualizations needed for robotics.

**Configuration**:
```javascript
themes: ['@docusaurus/theme-mermaid'],
markdown: { mermaid: true }
```

**Sources**:
- [Docusaurus Diagrams](https://docusaurus.io/docs/3.5.2/markdown-features/diagrams)

---

## 6. Mobile Design: Responsive (Docusaurus Default)

### Decision: Mobile-first responsive design using Docusaurus defaults

**Rationale**: Docusaurus is mobile-first by default. Custom optimizations focus on content formatting rather than framework changes.

**Mobile Optimizations**:
- Keep code lines under 80 characters when possible
- Use inline math for simple equations
- Responsive image sizing in Markdown
- Viewport configuration for safe-area support

**Configuration**:
```javascript
metadata: [{
  name: 'viewport',
  content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no',
}]
```

**Sources**:
- [Docusaurus Styling and Layout](https://docusaurus.io/docs/next/styling-layout)
- [Mobile Safe-Area Support](https://stackoverflow.com/questions/73249907)

---

## 7. Deployment: GitHub Actions with Official Workflow

### Decision: Use official Docusaurus GitHub Actions workflow

**Rationale**: Battle-tested, maintained by Docusaurus team, supports GitHub Pages deployment with OIDC permissions.

**Workflow**:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - name: Install dependencies
        run: npm ci
      - name: Build Docusaurus
        run: npm run build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./build
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**GitHub Pages Configuration**:
- Source: `/(root)` and `/build` directory
- Base URL configured in `docusaurus.config.js`

**Sources**:
- [Docusaurus Deployment](https://docusaurus.io/docs/deployment)
- [GitHub Actions Deployment Discussion](https://github.com/facebook/docusaurus/discussions/11254)

---

## 8. Spec-Kit Plus Integration

### Decision: Standard Spec-Kit Plus directory structure with Docusaurus docs/

**Directory Structure**:
```text
project-root/
├── .claude/                  # Claude Code subagents
├── .specify/                 # SDD configuration
├── specs/                    # Feature specifications
│   └── 001-textbook-platform/
├── docs/                     # Docusaurus content
├── history/                  # Prompt History Records
├── CLAUDE.md                 # Project instructions
├── docusaurus.config.js      # Docusaurus configuration
└── sidebars.js              # Navigation structure
```

**Spec-to-Content Linkage**:
- Lessons reference their spec via YAML frontmatter
- `spec_id` field links to `specs/###-feature/spec.md`
- `requirement_ids` map to FR numbers

**Sources**:
- [Spec-Kit Plus GitHub](https://github.com/panaversity/spec-kit-plus)
- [Medium: Claude Code, SpecKit Plus & Docusaurus](https://medium.com/@kulsoom0324/claude-code-speckit-plus-docusaurus-b8499b4350c9)

---

## 9. Subagent Format Requirements

### Decision: Strict YAML format for Claude Code subagents

**Valid Fields ONLY**: `name`, `description`, `tools`, `model`, `skills`

**CRITICAL Format Rules**:
- Single-line descriptions only (multi-line breaks parsing)
- Comma-separated tools/skills (YAML arrays break access)

**Correct Format**:
```yaml
---
name: content-implementer
description: Educational content generator with MANDATORY skill invocation. Use for lessons/chapters with YAML frontmatter.
model: opus
tools: Read, Grep, Glob, Edit, Write
skills: ai-collaborate-teaching, learning-objectives, content-evaluation-framework
---
```

**Anti-Patterns to Avoid**:
- Multi-line descriptions with `|`
- YAML arrays for tools: `tools: [Read, Grep]`
- "Should I proceed?" confirmation requests
- Returning full content instead of writing files

**Sources**:
- [Claude Code Subagent Documentation](https://code.claude.com/docs/en/sub-agents)
- [AGENTS.md Format Reference](https://agents.md/)

---

## 10. Content Quality Gates

### Decision: Educational-validator with constitutional compliance checks

**Required Checks**:
1. **Framework Invisibility**: No meta-commentary like "Part 2: AI as Teacher"
2. **Evidence Presence**: 70%+ of code blocks have `**Output:**` sections
3. **Structural Compliance**: Lessons end with `## Try With AI`, no summary after
4. **Proficiency Alignment**: Cognitive load matches declared CEFR level

**6-Category Rubric**:
1. Technical Accuracy (30%)
2. Pedagogical Effectiveness (25%)
3. Writing Quality (20%)
4. Structure & Organization (15%)
5. AI-First Teaching (10%)
6. Constitution Compliance (Pass/Fail)

**Sources**:
- [Constitution: `.specify/memory/constitution.md`](../.specify/memory/constitution.md)

---

## 11. Version Tracking

| Decision | Chosen | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Docusaurus version | 3.9 | 3.x earlier, Hugo, Next.js | AI search, i18n support |
| Content organization | Single instance with categories | Multi-instance | Simpler for launch |
| Math rendering | KaTeX | MathJax | Performance, native support |
| Code theme | Palenight/GitHub | Dracula, Duotone | Robotics language support |
| Diagrams | Hybrid Mermaid + images | Mermaid only, images only | Text-based + complex visuals |
| Deployment | GitHub Actions | Manual, Netlify, Vercel | Free, integrated with GitHub |

---

## 12. Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Docusaurus version for 2025 | Use 3.9 for AI search features |
| Math rendering choice | KaTeX for performance |
| Code highlighting theme | Palenight (dark) / GitHub (light) |
| Diagram approach | Mermaid for simple, images for complex |
| Mobile reading experience | Responsive Docusaurus defaults |
| CI/CD deployment | Official GitHub Actions workflow |
| Spec-Kit Plus directory layout | Standard structure with docs/ integration |
| Subagent YAML format | Single-line descriptions only |

---

## 13. Next Steps (Phase 1)

1. Create `data-model.md` with content entity definitions
2. Create `contracts/` directory with YAML frontmatter schema
3. Create `quickstart.md` for new content authors
4. Update agent context with technology stack
5. Re-evaluate Constitution Check post-design

---

**Research Status**: COMPLETE | All NEEDS CLARIFICATION items resolved
