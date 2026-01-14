---
prompt_id: "PHR-003"
date: 2025-01-13
stage: plan
title: plan-creation-textbook-platform
feature: textbook-platform
tags: ["plan", "docusaurus", "research-concurrent", "phase-0", "phase-1"]
---

# Prompt: Plan Creation - Textbook Platform

**Stage**: plan
**Feature**: textbook-platform
**Date**: 2025-01-13
**ID**: PHR-003

## PROMPT_TEXT

```
/sp.plan

You are creating an implementation plan for Phase 1 of the Physical AI & Humanoid Robotics Textbook project.

## Project Context

**Goal**: Create an AI-native educational platform teaching Physical AI & Humanoid Robotics using Spec-Kit Plus, Claude Code, and Docusaurus with GitHub Pages deployment.

**Course**: AI Systems in the Physical World - Embodied Intelligence (13-week curriculum)

**Target Audience**: Students and professionals learning to build, simulate, and deploy humanoid robots using ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action models.

**Course Structure**:
- Weeks 1-2: Introduction to Physical AI (sensors, embodied intelligence)
- Weeks 3-5: ROS 2 Fundamentals (nodes, topics, services, URDF, rclpy)
- Weeks 6-7: Robot Simulation (Gazebo, Unity, SDF, physics)
- Weeks 8-10: NVIDIA Isaac Platform (Isaac Sim, Isaac ROS, VSLAM, Nav2, RL)
- Weeks 11-12: Humanoid Development (kinematics, bipedal locomotion, HRI)
- Week 13: Conversational Robotics (voice commands, GPT, VLA models)

**Hackathon Requirements**:
- Base: Docusaurus book deployed to GitHub Pages (100 points)
- Bonus: Claude Code subagents/skills (+50), Better Auth (+50), Content personalization (+50), Urdu translation (+50)

---

## Instructions

Create a comprehensive implementation plan that includes:

### 1. Architecture Sketch
- Docusaurus site structure (docs/, blog, static assets)
- GitHub Actions CI/CD for auto-deployment
- Spec-Kit Plus integration (specs/, .specify/ directory)
- Claude Code workflow (.claude/agents, .claude/skills)
- Navigation hierarchy reflecting course modules

### 2. Section Structure
Break down the book into:
- **Front matter**: About this course, prerequisites, hardware guide, how to use this book
- **4 Main Modules** corresponding to course weeks above
- **Appendices**: ROS 2 cheat sheet, troubleshooting, glossary, references
- **Chapter template** (YAML frontmatter, narrative opening, technical content, Try With AI prompts)

### 3. Research Approach
- Identify authoritative sources (ROS 2 docs, NVIDIA Isaac docs, Gazebo docs)
- Hardware verification protocol (RTX GPUs, Jetson specs, RealSense, robot platforms)
- Version compatibility checks (ROS 2 Humble vs Iron vs Jazzy)
- Image/diagram sourcing strategy

### 4. Quality Validation
- YAML frontmatter completeness checklist
- Code example validation (must run/test before inclusion)
- Hardware requirement flags (simulation-only vs physical hardware)
- Subagent usage requirement (content-implementer, educational-validator)
- Citation style (APA per Constitution)

### 5. Decisions Needing Documentation
For each decision, list:
- **Decision**: What needs to be chosen
- **Options**: Available alternatives
- **Tradeoffs**: Pros/cons of each
- **Recommendation**: Suggested path with rationale

Key decisions to address:
- Docusaurus version (v3.x features, compatibility)
- Math rendering (KaTeX vs MathJax)
- Code block syntax highlighting themes
- Diagram generation (Mermaid, external images, ASCII)
- Mobile-first vs desktop-first reading experience

### 6. Testing Strategy
Validation checks based on acceptance criteria:
- [ ] Site builds locally (`npm run build`)
- [ ] Site deploys to GitHub Pages
- [ ] All internal links resolve
- [ ] Code blocks are syntax-highlighted correctly
- [ ] Math equations render properly
- [ ] Navigation follows course progression
- [ ] Each lesson has complete YAML frontmatter
- [ ] Hardware requirements specified per lesson
- [ ] Try With AI prompts present in every lesson

---

## Technical Details

**Use research-concurrent approach**: Research while writing, not all upfront. Iterate on content as you verify technical details.

**Follow APA citation style** from Constitution (`.specify/memory/constitution.md`)

**Organize by phases**:
1. **Research** → 2. **Foundation** (site setup, templates) → 3. **Analysis** (content drafting) → 4. **Synthesis** (review, validate, deploy)

---

## Output Format

Write the plan as `docs/plans.md` using clear markdown sections, tables for comparisons, and checklists for verification steps. Make the plan actionable enough that another developer (or future you) can execute it step-by-step.
```

## RESPONSE_TEXT

Successfully created comprehensive implementation plan for AI/Spec-Driven Physical AI & Humanoid Robotics Textbook.

**Branch**: `001-textbook-platform`
**Plan File**: `specs/001-textbook-platform/plan.md`

### Phase 0: Research ✅ COMPLETE

Created `research.md` with technology decisions:
- **Docusaurus 3.9**: AI-powered search, i18n for Urdu translation
- **Content Organization**: Single instance with categorized modules (simpler than multi-instance)
- **Math Rendering**: KaTeX for performance (faster than MathJax)
- **Code Highlighting**: Palenight (dark) / GitHub (light) themes
- **Diagrams**: Hybrid Mermaid (simple diagrams) + external images (complex visualizations)
- **Deployment**: GitHub Actions with official Docusaurus workflow
- **Spec-Kit Plus**: Standard directory structure with docs/ integration

### Phase 1: Design ✅ COMPLETE

Created design artifacts:

**1. `data-model.md`**: Content entity definitions
- Module, Lesson, Code Example, Try With AI Prompt, Assessment entities
- YAML frontmatter schema with all required fields
- Entity relationships and file system schema
- State transitions for lesson lifecycle

**2. `contracts/` directory**: Schema contracts
- `lesson-frontmatter-schema.md`: Required YAML fields, enums, validation rules
- `content-structure-schema.md`: Required sections, prohibited elements, quality checklist

**3. `quickstart.md`**: Getting started guide for content authors
- Prerequisites and setup instructions
- Content creation workflow (spec → plan → tasks → implement)
- Lesson template with complete frontmatter example
- Common commands and troubleshooting

**4. `plan.md`**: Complete implementation plan
- Technical context (Docusaurus 3.9, Node.js 20, static site)
- Architecture sketches (content creation workflow, deployment, navigation)
- Decision documentation with tradeoff analysis
- Testing strategy (build, content quality, deployment, UAT)
- Implementation phases (Research ✅, Design ✅, Tasks →, Implementation)

### Constitution Check

| Principle | Status |
|-----------|--------|
| I. Spec-Driven Development | ✅ PASS |
| II. Educational Quality | ✅ PASS |
| III. Technical Accuracy | ✅ PASS |
| IV. Hardware-Awareness | ✅ PASS |
| V. Subagent Orchestration | ✅ PASS |

All principles maintained. No violations requiring justification.

### Key Technical Decisions Documented

1. **Docusaurus 3.9**: AI-powered search for content discoverability
2. **Single-instance docs**: Simpler launch, can migrate to multi-instance later
3. **KaTeX**: Pre-rendered at build time, faster than MathJax
4. **Palenight/GitHub themes**: Best contrast for Python/C++/YAML/bash
5. **Hybrid diagrams**: Mermaid for version-controlled architecture, images for screenshots

### Project Structure Defined

```
physical-ai-robotics-textbook/
├── docs/                     # Docusaurus content (6 modules)
├── .claude/                  # Subagents and skills
├── .specify/                 # Spec-Kit Plus configuration
├── specs/                    # Feature specifications
├── history/                  # Prompt History Records
├── docusaurus.config.js
├── sidebars.js
└── CLAUDE.md
```

## Outcome

- ✅ Impact: Complete technical plan with all research decisions, data model, contracts, and quickstart guide
- 🧪 Tests: Constitution compliance verified, all gates passed
- 📁 Files: 5 files created (research.md, data-model.md, 2 contracts, quickstart.md) + plan.md updated
- 🔁 Next prompts: `/sp.tasks` to generate task breakdown, `/sp.implement` to execute
- 🧠 Reflection: Research-concurrent approach worked well. All technology decisions made with authoritative sources. Ready for implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL):
  - Constitution Check: PASS
  - YAML Frontmatter Schema: COMPLETE
  - Content Structure Schema: COMPLETE
  - Data Model: COMPLETE
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate the lesson template by creating first lesson content using content-implementer subagent
