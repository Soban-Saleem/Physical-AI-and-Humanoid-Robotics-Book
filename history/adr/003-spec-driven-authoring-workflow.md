# ADR-003: Spec-Driven Authoring Workflow with Subagents

> **Scope**: Content creation methodology ensuring quality, consistency, and constitutional compliance across 50+ lessons.

- **Status:** Accepted
- **Date:** 2025-01-13
- **Feature:** textbook-platform
- **Context:** Educational content production requiring verified technical claims, YAML frontmatter, and quality gates

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - defines how ALL content is created
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 4 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - affects every lesson, all authors, entire content pipeline
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use Claude Code subagents with Spec-Kit Plus workflow for all educational content creation.**

**Authoring Pipeline:**
```
1. /sp.specify  → Create feature specification (user stories, FRs, SCs)
2. /sp.plan     → Create technical plan (architecture, decisions)
3. /sp.tasks    → Generate task breakdown
4. /sp.implement → Invoke content-implementer subagent
5. educational-validator → Constitutional compliance check
6. factual-verifier → Technical claim verification
7. PHR creation → Document conversation
8. Git commit → Deploy
```

**Required Subagents:**
- **content-implementer**: Generates lesson content with YAML frontmatter
- **educational-validator**: Checks constitutional compliance (framework invisibility, evidence presence, structural compliance, proficiency alignment)
- **factual-verifier**: Verifies technical claims against authoritative sources (ROS 2 docs, NVIDIA Isaac, hardware specs)
- **chapter-planner**: Designs lesson sequences with pedagogical progression
- **assessment-architect**: Generates quiz questions aligned to Bloom's taxonomy

**Critical Workflow Constraint:**
content-implementer MUST read 9 skills before generating content (blocking 30-60s):
- ai-collaborate-teaching
- learning-objectives
- content-evaluation-framework
- skills-proficiency-mapper
- exercise-designer
- [4 more applicable skills]

## Consequences

### Positive

- **Constitutional compliance enforced** - educational-validator blocks non-compliant content
- **Technical accuracy verified** - factual-verifier prevents hallucinated specs
- **Spec traceability** - every lesson links to origin spec via `spec_id` and `requirement_ids`
- **Reusable skills** - patterns scale across all 50+ lessons
- **Parallel development** - multiple authors can work on different modules simultaneously
- **Quality consistency** - all lessons follow same structure and standards
- **Reduced review burden** - validators catch issues before human review

### Negative

- **Slower first lesson** - subagent reads 9 skills blocking (30-60s)
- **Claude Code dependency** - authors need Claude Code access
- **YAML format strictness** - multi-line descriptions break tool parsing
- **No direct writing allowed** - constitution blocks direct lesson writing
- **Subagent invocation overhead** - must provide absolute paths, reference lessons
- **Learning curve** - authors must learn Spec-Kit Plus workflow

## Alternatives Considered

### Alternative A: Direct Human Writing
**Approach:** Authors write Markdown directly without subagents
**Why rejected:**
- Constitution REQUIRES subagent usage for educational content
- No quality gates - inconsistent frontmatter, missing fields
- No spec traceability - can't track which requirements lesson fulfills
- Chapter 2 incident showed 50% session waste without quality gates
- **Proven failure pattern** - direct writing caused quality drift in previous projects

### Alternative B: GPT-4 API Directly
**Approach:** Build custom scripts calling OpenAI API for content generation
**Why rejected:**
- Loses Claude Code subagent orchestration
- Must reimplement skill reading, validation, fact-checking
- No integration with Spec-Kit Plus workflow
- No educational-validator or factual-verifier equivalents
- **Reinventing wheel** - Claude Code already provides this infrastructure

### Alternative C: Traditional CMS (WordPress, Contentful)
**Approach:** Web-based CMS with forms for content entry
**Why rejected:**
- Authors must learn CMS interface instead of Markdown
- No Git version control for content
- No integration with Spec-Kit Plus or Claude Code
- YAML frontmatter must be custom-implemented
- **Workflow mismatch** - spec-driven workflow doesn't map to CMS forms

### Alternative D: No Quality Gates
**Approach:** Write content, validate manually before publishing
**Why rejected:**
- Constitution requires educational-validator checks
- Manual review doesn't scale to 50+ lessons
- No enforcement of framework invisibility or evidence presence
- Technical claims go unverified without factual-verifier
- **Hackathon criteria** - bonus points require subagent/skills usage

## YAML Format Constraints (Critical)

**CRITICAL:** Subagent YAML format is strict. Multi-line descriptions break tool parsing.

**Valid Format:**
```yaml
---
name: content-implementer
description: Single line description here (max 1024 chars)
tools: Read, Grep, Glob, Edit, Write
skills: skill1, skill2, skill3
---
```

**Invalid Formats (break parsing):**
```yaml
# ❌ Multi-line description
description: |
  Long description with
  multiple lines

# ❌ YAML array for tools
tools:
  - Read
  - Grep
```

## Lesson Frontmatter Requirements

Every lesson MUST include:

| Field | Required | Validation |
|-------|----------|------------|
| `sidebar_position` | Yes | Integer ≥ 1 |
| `title`, `description` | Yes | Non-empty strings |
| `keywords` | Yes | Array of 3-7 strings |
| `chapter`, `lesson` | Yes | Chapter: 1-6, Lesson: integer |
| `duration_minutes` | Yes | 15-180 |
| `requirements.hardware` | Yes | Hardware specifications |
| `requirements.software` | Yes | Software versions |
| `skills[]` | Yes | At least 1 with all 5 subfields |
| `learning_objectives[]` | Yes | At least 1 with all 4 subfields |
| `cognitive_load.new_concepts` | Yes | Integer matching CEFR level |
| `differentiation.*` | Yes | All 3 fields required |
| `spec_id` | Yes | Must reference existing spec |
| `requirement_ids` | Yes | Must map to spec FRs |

## Content Structure Requirements

Every lesson MUST contain:
1. **Narrative opening** (2-3 paragraphs) - real-world scenario connection
2. **Technical content** - code examples with `**Output:**` blocks
3. **Hardware context** - requirements + simulation alternatives
4. **Three "Try With AI" prompts** - each with "**What you're learning:**"
5. **End with action** - `## Try With AI` is LAST section (no summary after)

**Prohibited:**
- ❌ "## Summary" after Try With AI
- ❌ "## Key Takeaways" after Try With AI
- ❌ Framework labels ("Part 1: AI as Teacher", etc.)

## Failure Prevention (Learned from Incidents)

| Failure Pattern | Consequence | Prevention |
|-----------------|-------------|------------|
| Missing YAML fields | Validation fails | educational-validator checks all required fields |
| Multi-line YAML descriptions | Subagent breaks | Single-line descriptions only |
| Code without Output | Evidence claims fail | 70%+ code blocks must have Output blocks |
| Summary after Try With AI | Constitution violation | End with action only |
| Returning content instead of writing files | Context bloat | Subagents write directly, return confirmation only |

## References

- Feature Spec: [spec.md](../specs/001-textbook-platform/spec.md)
- Implementation Plan: [plan.md](../specs/001-textbook-platform/plan.md)
- Constitution: [.specify/memory/constitution.md](../.specify/memory/constitution.md)
- Contracts: [contracts/](../specs/001-textbook-platform/contracts/)
- Related ADRs: ADR-001 (Static Site Platform), ADR-002 (Content Organization)
