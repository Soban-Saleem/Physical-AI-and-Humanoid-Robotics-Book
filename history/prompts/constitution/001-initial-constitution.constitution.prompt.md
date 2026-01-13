---
id: 001
title: Initial Constitution for Physical AI Robotics Textbook
stage: constitution
date: 2026-01-13
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: TBD
command: /sp.constitution
labels: ["constitution","setup","sdd"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - CLAUDE.md
tests:
  - N/A (constitution creation)
---

## Prompt

Project: Physical AI & Humanoid Robotics AI-Native Textbook. Phase 1: AI/Spec-Driven Book Creation using Docusaurus and GitHub Pages.

Core principles:
- Spec-Driven Development using Spec-Kit Plus workflow
- Educational quality with constitutional compliance (framework invisibility, evidence presence)
- Technical accuracy via primary source verification
- Hardware-aware content with simulation alternatives
- Subagent orchestration for all educational content

Key standards:
- Full YAML frontmatter (skills, learning objectives, cognitive load, differentiation, requirements)
- Three "Try With AI" prompts per lesson
- Code examples with Output blocks
- End with action (no Summary after Try With AI)
- ROS 2/Isaac/hardware specs verified from official docs

Success criteria:
- All 4 modules published to GitHub Pages
- Every lesson passes educational-validator
- All technical claims fact-checked
- Hardware alternatives provided

## Response snapshot

Created comprehensive constitution v1.0.0 for Physical AI & Humanoid Robotics Textbook with 5 core principles:

1. **I. Spec-Driven Development (NON-NEGOTIABLE)**: All content follows Spec-Kit Plus workflow (Specification → Plan → Tasks → Implementation)

2. **II. Educational Quality (CONSTITUTIONAL COMPLIANCE)**: Four constitutional checks (Framework Invisibility, Evidence Presence, Structural Compliance, Proficiency Alignment)

3. **III. Technical Accuracy (PRIMARY SOURCE VERIFICATION)**: All technical claims verified against authoritative sources (ROS 2 docs, NVIDIA Isaac, manufacturer specs)

4. **IV. Hardware-Awareness (ALWAYS PROVIDE ALTERNATIVES)**: Must provide simulation/cloud alternatives for students without physical hardware

5. **V. Subagent Orchestration (EDUCATIONAL CONTENT ONLY)**: Educational content MUST use content-implementer + educational-validator (direct writing blocked)

Also defined:
- Complete YAML frontmatter template
- Content structure requirements (narrative opening, technical content, hardware context, 3 Try With AI prompts, end with action)
- Three Roles Framework for L2 lessons
- Technology stack (Docusaurus, Spec-Kit Plus, Claude Code)
- Constraints (word count, proficiency progression, platform)
- Success criteria (content quality, accessibility, completeness)
- Governance (amendment process, versioning, compliance review)

File created: `.specify/memory/constitution.md`

## Outcome

- ✅ Impact: Established project constitution as source of truth for all content creation
- 🧪 Tests: N/A (constitution creation)
- 📁 Files: .specify/memory/constitution.md (276 lines)
- 🔁 Next prompts: /sp.specify for Module 1 (ROS 2 Fundamentals)
- 🧠 Reflection: Constitution provides guardrails for the 13-week curriculum development, ensuring educational quality and technical accuracy throughout the hackathon timeline

## Evaluation notes (flywheel)

- Failure modes observed: None (initial creation)
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create Module 1 specification using /sp.specify
