---
prompt_id: "PHR-001"
date: 2025-01-13
stage: spec
title: spec-creation-textbook-platform
feature: textbook-platform
tags: ["specification", "docusaurus", "rag-chatbot", "educational-platform"]
---

# Prompt: Specification Creation - Textbook Platform

**Stage**: spec
**Feature**: textbook-platform
**Date**: 2025-01-13
**ID**: PHR-001

## PROMPT_TEXT

```
/sp.specify AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

Target audience: University students and professionals learning Physical AI, robotics engineers, developers building embodied AI systems
Focus: Creating an interactive educational platform teaching ROS 2, simulation, NVIDIA Isaac, and humanoid robotics with integrated RAG chatbot

Success criteria:
- Working Docusaurus site deployed to GitHub Pages
- Module 1 (Introduction to Physical AI) fully written with 4-5 lessons
- Integrated RAG chatbot using FastAPI, Qdrant, and OpenAI Agents
- Spec-Kit Plus templates configured for all content types (lessons, chapters, assessments)
- Claude Code subagents and skills created for educational content generation
- All content follows 4-Layer Teaching Method (L1-L4)
- Full YAML frontmatter on every lesson (skills metadata, learning objectives, cognitive load)
- Content verified with educational-validator before publication

Constraints:
- Platform: Docusaurus 3.x deployed to GitHub Pages
- Content format: Markdown with YAML frontmatter
- Auth: Better Auth integration for signup/signin
- Timeline: Complete base functionality by November 30, 2025
- Content must be hardware-aware (RTX GPU, Jetson, sensors)
- All technical claims verified via WebSearch before inclusion
- Educational content MUST use content-implementer subagent (no direct writing)

Not building:
- Mobile apps (mobile-responsive web only)
- Full course platform (LMS features, grading, certificates)
- Physical robot hardware (focus on simulation with optional hardware)
- Video hosting (embed external only)
- Peer review or collaboration features
- Payment processing or course sales
```

## RESPONSE_TEXT

Created specification for AI/Spec-Driven Physical AI & Humanoid Robotics Textbook platform.

**Branch**: `001-textbook-platform`
**Spec File**: `specs/001-textbook-platform/spec.md`
**Checklist**: `specs/001-textbook-platform/checklists/requirements.md`

**User Stories Defined** (4 prioritized, independently testable):
1. **P1**: Browse and Learn Course Content - Core content delivery
2. **P2**: Ask AI Questions About Content - RAG chatbot interaction
3. **P3**: Sign Up and Track Learning Progress - Authentication and progress
4. **P2**: Authors Create Spec-Driven Content - Subagent-powered authoring

**Functional Requirements**: 25 testable requirements across content delivery, AI chatbot, authentication, content creation, content standards, and deployment.

**Success Criteria**: 10 measurable outcomes including page load times (<2s), chatbot relevance (80%), signup time (<3min), and content generation time (<30min).

**Validation Status**: PASSED
- All mandatory sections complete
- Requirements are testable and unambiguous
- Success criteria are technology-agnostic and measurable
- No [NEEDS CLARIFICATION] markers
- Scope clearly bounded with "Out of Scope" section

**Next Steps**: Run `/sp.clarify` to explore any remaining questions, or proceed to `/sp.plan` to create implementation plan.
