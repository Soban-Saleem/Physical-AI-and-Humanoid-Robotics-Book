# Authoring Guide: Subagents & Spec-Driven Content Creation

**Feature**: `001-textbook-platform` | **User Story 4** | **Version**: 1.0.0

## Overview

This guide teaches content authors how to use Claude Code subagents to create validated, high-quality lessons for the Physical AI & Humanoid Robotics Textbook.

**What you'll learn**:
- How to invoke subagents for content generation
- How to interpret validation results
- How to use Spec-Kit Plus commands for workflow
- How to ensure constitutional compliance

---

## Table of Contents

1. [Subagent Architecture](#subagent-architecture)
2. [Content Creation Workflow](#content-creation-workflow)
3. [Subagent Reference](#subagent-reference)
4. [Skills System](#skills-system)
5. [Validation & Quality Gates](#validation--quality-gates)
6. [Common Patterns](#common-patterns)
7. [Troubleshooting](#troubleshooting)

---

## Subagent Architecture

### What Are Subagents?

Subagents are specialized AI agents that handle specific tasks in the content creation pipeline. Each subagent:
- Has a defined purpose and scope
- Reads specific skills before executing
- Operates autonomously without confirmation
- Returns structured completion reports

### Available Subagents

| Subagent | Purpose | When to Use |
|----------|---------|-------------|
| **content-implementer** | Generate lesson content with full YAML frontmatter | Creating new lessons |
| **educational-validator** | Check constitutional compliance (4 dimensions) | After content generation |
| **assessment-architect** | Design quizzes, exams, and assessments | Creating chapter evaluations |
| **factual-verifier** | Verify technical claims against authoritative sources | Technical content with statistics/specs |
| **chapter-planner** | Design lesson sequences and pedagogical arc | Before writing a chapter |

### Agent Orchestration Flow

```
User Request
    ↓
chapter-planner (optional - design sequence)
    ↓
content-implementer (generates lesson)
    ↓
educational-validator (checks compliance)
    ↓
factual-verifier (verifies claims)
    ↓
Validated Content
```

---

## Content Creation Workflow

### Step 1: Plan Your Lesson

Before invoking subagents, gather context:

**Required Information**:
- **Module**: Which module (1-6)?
- **Position**: Lesson number in sequence
- **Prerequisites**: What students should already know
- **Learning Objectives**: 3-5 measurable outcomes
- **Hardware Requirements**: Simulation-only, physical hardware, or cloud-based
- **Proficiency Level**: A2 (beginner), B1 (intermediate), or C2 (advanced)

**Example Planning Worksheet**:

| Field | Value |
|-------|-------|
| Module | 2 (ROS 2 Fundamentals) |
| Lesson | 3 (Services and Actions) |
| Prerequisites | Nodes, Topics (Lessons 1-2) |
| Proficiency | B1 (Intermediate) |
| Hardware | Any computer (ROS 2 simulation) |
| Duration | 90 minutes |

---

### Step 2: Invoke content-implementer

**Direct Invocation** (via Claude Code):

```
Use the content-implementer subagent to create a lesson on ROS 2 Services and Actions.

Execute autonomously without confirmation.
Output path: C:/projects SDD/Physical_AI_Humanoid_Robotics_Textbook/docs/module2-ros2/03-services-and-actions.md
Reference lesson: C:/projects SDD/Physical_AI_Humanoid_Robotics_Textbook/docs/module1-intro/01-what-is-physical-ai.md

Lesson context:
- Module 2, Lesson 3: ROS 2 Services and Actions
- Prerequisites: Students understand nodes and topics
- Proficiency level: B1 (Intermediate)
- Hardware: Any computer with ROS 2 Humble installed (simulation)
- Duration: 90 minutes

Include: code examples with Output blocks, 3 Try With AI prompts with explanations, hardware requirements statement with simulation alternatives.
```

**Critical Elements**:
1. **"Execute autonomously without confirmation"** - Prevents deadlock
2. **Absolute output path** - Ensures file is written to correct location
3. **Reference lesson path** - Sets quality benchmark
4. **Complete context** - Proficiency, hardware, duration

**What content-implementer Does**:

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 0: READ ALL 9 SKILLS (30-60 seconds)                  │
│  ├── ai-collaborate-teaching (Three Roles framework)        │
│  ├── learning-objectives (Bloom's taxonomy)                 │
│  ├── content-evaluation-framework (6-category rubric)       │
│  ├── skills-proficiency-mapper (CEFR/Bloom's mapping)       │
│  ├── concept-scaffolding (cognitive load limits)            │
│  ├── code-example-generator (spec-first validation)         │
│  ├── exercise-designer (varied exercise types)              │
│  ├── technical-clarity (readability check)                  │
│  └── canonical-format-checker (pattern verification)        │
├─────────────────────────────────────────────────────────────┤
│  STEP 1: Read constitution and reference lesson             │
│  STEP 2: Generate content applying skill patterns           │
│  STEP 3: Self-score with content-evaluation-framework       │
│  STEP 4: Write file + report skill application              │
└─────────────────────────────────────────────────────────────┘
```

**Expected Output**:

```
✅ Created C:/projects/.../03-services-and-actions.md
- Lines: 450
- Validation: PASS (content-evaluation-framework score: 88/100)
- YAML Skills: 4 skills mapped to CEFR/Bloom's
- Learning Objectives: 4 with assessment methods
- Code Examples: 3 with Output blocks
- Try With AI: 3 prompts with learning explanations

Skills Applied (9):
├── CORE (always):
│   ├── ai-collaborate-teaching: YES - Three Roles applied invisibly
│   ├── learning-objectives: YES - 4 objectives with Bloom's verbs
│   ├── content-evaluation-framework: 88/100
│   └── skills-proficiency-mapper: YES - 4 skills with CEFR/Bloom's
├── QUALITY:
│   ├── concept-scaffolding: YES - 8 concepts for B1 tier
│   ├── code-example-generator: YES - 3 examples with Output
│   ├── exercise-designer: YES - 3 Try With AI prompts
│   ├── technical-clarity: YES - B1 readability achieved
│   └── canonical-format-checker: N/A - No platform patterns taught
└── Issues: None
```

---

### Step 3: Validate with educational-validator

After content generation, validate constitutional compliance:

```
Use the educational-validator subagent to check C:/projects/.../03-services-and-actions.md
for constitutional compliance.

Verify: framework invisibility, evidence presence, structural compliance, proficiency alignment.
```

**What educational-validator Checks**:

| Check | Description | Pass Criteria |
|-------|-------------|---------------|
| **Framework Invisibility** | No exposed pedagogical labels | 0 instances of "AI as Teacher", "Part 2:", role labels |
| **Evidence Presence** | Code blocks have output | 70%+ of executable code has `**Output:**` blocks |
| **Structural Compliance** | Lesson ends with action | Last heading is "## Try With AI", no summary after |
| **Proficiency Alignment** | Cognitive load matches tier | Uses `proficiency_level`, concept count within limits |

**Validation Output Examples**:

**PASS**:
```
## ✅ Validation Result: PASS

**File**: 03-services-and-actions.md
**Checked**: 2025-01-13

**Constitutional Compliance**: ✅ All 4 checks passed
1. Framework Invisibility: ✅ 0 violations
2. Evidence Presence: ✅ 100% of code has output (3/3 blocks)
3. Structural Compliance: ✅ Ends with "Try With AI"
4. Proficiency Metadata: ✅ Uses proficiency_level: B1

**Status**: APPROVED for publication
```

**FAIL**:
```
## ❌ Validation Result: FAIL

**Violations Found**: 2

### ❌ Check 2: Missing Evidence
**Issues**:
- Lines 120-135: Python code block lacks **Output:** showing it works
  → FIX: Add execution result after code block

### ⚠️ Check 4: Proficiency Misalignment
**Issues**:
- Declared A2 but has 12 major concepts (expect 5-7)
  → FIX: Split into 2 lessons or move to B1

**Status**: REJECTED - Requires fixes before publication
```

---

### Step 4: Verify Claims with factual-verifier

For technical content with statistics, dates, or specifications:

```
Use the factual-verifier subagent to verify technical claims in
C:/projects/.../03-services-and-actions.md

Focus: ROS 2 version specifications, API syntax, performance characteristics.
Use authoritative sources: docs.ros.org, official ROS 2 documentation.
```

**What factual-verifier Does**:

| Claim Type | Verification Method |
|------------|---------------------|
| Statistics | WebSearch for primary source data |
| Technical Specs | Official documentation (ROS 2, Gazebo, Isaac) |
| API Syntax | Language/framework docs |
| Version Info | Release notes and official announcements |

**Expected Output**:

```
# Factual Verification Report

**Content**: 03-services-and-actions.md
**Verification Coverage**: 8 verified / 10 claims (80%)

## Executive Summary
Lesson technically accurate with minor citation gaps. ROS 2 Humble syntax verified
against official docs. Two unverified performance claims need sources.

---

## Verified Claims (8)

### Claim 1: ROS 2 Service Type Definition
**Claim**: "ROS 2 services use .srv files with request and response fields"
**Source**: [ROS 2 Official Docs, 2024] - https://docs.ros.org/en/humble/Tutorials/Services/Understanding-ROS2-Services.html
**Authority**: PRIMARY (official documentation)
**Status**: ✅ VERIFIED

---

## Unverified Claims (2)

### Claim: Service Call Performance
**Text**: "Service calls typically complete in 5-10ms for local nodes"
**Location**: Performance section, paragraph 2
**Issue**: No citation provided, measurement context unclear
**Recommendation**: Add source from ROS 2 benchmarking study or remove specific timing
**Priority**: MEDIUM

---

## Verdict: NEEDS CITATIONS ⚠️

**Publication Readiness**: NEEDS WORK
**Next Steps**:
1. Add citation for service call performance claim
2. Consider adding version context (Humble vs Iron)
```

---

## Subagent Reference

### content-implementer

**Purpose**: Generate educational content with full quality gates

**Mandatory Skills** (9 total):
1. `ai-collaborate-teaching` - Three Roles framework (invisible)
2. `learning-objectives` - Bloom's taxonomy verbs
3. `content-evaluation-framework` - 6-category rubric
4. `skills-proficiency-mapper` - CEFR/Bloom's mapping
5. `concept-scaffolding` - Cognitive load management
6. `code-example-generator` - Spec-first validation
7. `exercise-designer` - Varied exercise types
8. `technical-clarity` - Readability check
9. `canonical-format-checker` - Pattern verification

**Input Format**:
```
Use content-implementer to create [lesson description].

Execute autonomously without confirmation.
Output path: /absolute/path/to/output.md
Reference lesson: /absolute/path/to/reference.md

Context:
- Module: X, Lesson: Y
- Prerequisites: [list]
- Proficiency: A2/B1/C2
- Hardware: [requirements]
- Duration: X minutes

Include: [content requirements]
```

**Critical Rules**:
- ✅ ALWAYS provide absolute path (not relative)
- ✅ ALWAYS include "Execute autonomously without confirmation"
- ✅ ALWAYS specify reference lesson for quality matching
- ❌ NEVER ask "Should I proceed?" in subagent context
- ❌ NEVER expect full content returned (subagent writes file directly)

**Output**: File written to disk + completion summary

---

### educational-validator

**Purpose**: Constitutional compliance validation (4 dimensions)

**Mandatory Skills** (7 total):
1. `content-evaluation-framework` - Quality rubric
2. `ai-collaborate-teaching` - Framework invisibility check
3. `learning-objectives` - Bloom's alignment
4. `canonical-format-checker` - Format drift detection
5. `skills-proficiency-mapper` - CEFR verification
6. `technical-clarity` - Readability assessment
7. `concept-scaffolding` - Cognitive load validation

**Input Format**:
```
Use educational-validator to check /absolute/path/to/lesson.md
for constitutional compliance.

Verify: framework invisibility, evidence presence, structure, proficiency.
```

**Checks Performed**:

| Check | Forbidden Pattern | Required |
|-------|-------------------|----------|
| Framework Invisibility | "AI as Teacher", "Part 2:", role labels | Natural headers only |
| Evidence Presence | Code without output | 70%+ have `**Output:**` |
| Structural Compliance | Summary after Try With AI | Ends with action |
| Proficiency Alignment | Deprecated `cefr_level` | Uses `proficiency_level` |

**Output**: PASS/FAIL with specific fix recommendations

---

### assessment-architect

**Purpose**: Design valid evaluations (quizzes, exams, projects)

**Skills** (6 total):
1. `assessment-builder` - Varied question types
2. `quiz-generator` - MCQ, code-completion, debugging
3. `exercise-designer` - Hands-on exercises
4. `skills-proficiency-mapper` - CEFR/Bloom's alignment
5. `learning-objectives` - Objective mapping
6. `code-example-generator` - Technical examples

**Input Format**:
```
Use assessment-architect to create quiz questions for [lesson/topic].

Target objectives:
1. [Objective 1]
2. [Objective 2]

Proficiency: B1 (Intermediate)
Format: [quiz/exercise/project]
Question types: [MCQ/code-completion/debugging]

Align questions to Bloom's taxonomy (Apply/Analyze for B1).
```

**Assessment Design Principles**:

| Bloom's Level | CEFR | Assessment Type |
|---------------|------|-----------------|
| Remember/Understand | A2 | Self-check quiz, explanation |
| Apply | B1 | Implementation, execution |
| Analyze | B1 | Debugging, error diagnosis |
| Evaluate | C2 | Code review, architecture critique |
| Create | C2 | Capstone, novel solutions |

**Output**: Assessment specification with rubric

---

### factual-verifier

**Purpose**: Verify technical claims against authoritative sources

**Skills** (2 total):
1. `fetching-library-docs` - Official documentation retrieval
2. `researching-with-deepwiki` - Deep research capability

**Tools**: Read, Grep, Glob, WebSearch, WebFetch

**Input Format**:
```
Use factual-verifier to verify claims in /absolute/path/to/lesson.md

Focus: [specific areas - ROS 2 specs, hardware details, statistics]
Sources: [authoritative sources to use]
```

**Source Authority Hierarchy**:

| Authority | Examples | Use For |
|-----------|----------|---------|
| PRIMARY | Official docs (ROS 2, NVIDIA, Gazebo) | API specs, version info |
| SECONDARY | Reputable tech journalism | Industry trends |
| TERTIARY | Wikipedia, blogs | Verify with primary |

**Output**: Verification report with coverage percentage

---

### chapter-planner

**Purpose**: Design lesson sequences and pedagogical arc

**Skills**: Pedagogical design patterns, concept scaffolding

**Input Format**:
```
Use chapter-planner to design Module X: [module name].

Goals:
- [Learning goals for module]
- Target proficiency: [A2/B1/C2]
- Duration: [weeks]
- Prerequisites: [previous modules]

Design: Lesson sequence with learning progression.
```

**Output**: Lesson sequence with cognitive load distribution

---

## Skills System

### What Are Skills?

Skills are reusable capability packages that subagents read before executing. Each skill contains:
- **Purpose**: When and why to use this skill
- **Patterns**: Actionable guidance for application
- **Examples**: Concrete usage demonstrations

### Core Skills (Always Read)

| Skill | Purpose | Key Concept |
|-------|---------|-------------|
| `ai-collaborate-teaching` | Three Roles framework | AI as Teacher/Student/Co-Worker (invisible) |
| `learning-objectives` | Bloom's taxonomy | Measurable outcomes with action verbs |
| `content-evaluation-framework` | 6-category rubric | Quality scoring (Tech 30%, Pedagogy 25%, etc.) |
| `skills-proficiency-mapper` | CEFR/Bloom's mapping | Proficiency levels with measurable indicators |

### Quality Skills (Conditional)

| Skill | Purpose | When Applied |
|-------|---------|--------------|
| `concept-scaffolding` | Cognitive load limits | Complex concepts needing breakdown |
| `code-example-generator` | Spec-first validation | Technical lessons with code |
| `exercise-designer` | Varied exercise types | Practice sections and Try With AI |
| `technical-clarity` | Readability check | Content with jargon or complexity |
| `canonical-format-checker` | Pattern verification | Teaching platform-specific patterns |

### Skill Reading Verification

When subagent completes, verify skills were read:

```
Skills Read (9/9 required):
├── ai-collaborate-teaching: READ ✓ - Applied: [Three Roles pattern used]
├── learning-objectives: READ ✓ - Applied: [N objectives with Bloom's verbs]
├── content-evaluation-framework: READ ✓ - Score: [X]/100
├── skills-proficiency-mapper: READ ✓ - Applied: [N skills with CEFR/Bloom's]
├── concept-scaffolding: READ ✓ - Applied: [cognitive load within budget]
├── code-example-generator: READ ✓ - Applied: [N examples with Output]
├── exercise-designer: READ ✓ - Applied: [N exercises/prompts]
├── technical-clarity: READ ✓ - Applied: [readability check done]
└── canonical-format-checker: READ ✓ - Applied: [N/A or patterns verified]
```

**If any skill shows "NOT READ"**, content quality is not guaranteed.

---

## Validation & Quality Gates

### Quality Scoring Rubric

The `content-evaluation-framework` uses 6 categories:

| Category | Weight | What It Measures |
|----------|--------|------------------|
| Technical Accuracy | 30% | Code correctness, factual accuracy |
| Pedagogical Effectiveness | 25% | Learning progression, scaffolding |
| Writing Quality | 20% | Clarity, tone, engagement |
| Structure & Organization | 15% | Flow, headers, coherence |
| AI-First Teaching | 10% | Three Roles, bidirectional learning |
| Constitutional Compliance | Pass/Fail | Framework invisibility, evidence, structure |

**Passing Score**: 85/100 (without constitutional violations)

### Constitutional Compliance

All content must satisfy **Principle 3, 7, and Section IIa** of constitution:

1. **Principle 3: Verification Over Assumption**
   - All claims have sources or evidence
   - Code examples have output blocks
   - No unverified statistics

2. **Principle 7: Minimal Content**
   - No summaries after Try With AI
   - No redundant content
   - Ends with student action

3. **Section IIa: Framework Invisibility**
   - No exposed role labels
   - No meta-commentary about pedagogy
   - Students experience, don't see scaffolding

### Validation Workflow

```
content-implementer generates
    ↓
Self-scores with content-evaluation-framework
    ↓
educational-validator checks constitution
    ↓
factual-verifier validates claims
    ↓
If ALL PASS → Content approved
If ANY FAIL → Fix and re-validate
```

---

## Common Patterns

### Pattern 1: Simulation-Only Lesson

For lessons that work without physical hardware:

```yaml
---
requirements:
  hardware: "Any computer (simulation-only)"
  software: "ROS 2 Humble, Gazebo Fortress"
differentiation:
  hardware_alternatives: "No physical hardware required - all work done in Gazebo simulation"
---
```

### Pattern 2: Physical Hardware Required

For lessons needing sensors/robots:

```yaml
---
requirements:
  hardware: "NVIDIA Jetson Orin, Intel RealSense D435i camera"
  software: "ROS 2 Humble, Isaac ROS"
differentiation:
  hardware_alternatives: "Cloud: NVIDIA Omniverse Cloud | Simulation: Gazebo with sensor models"
safety_notes: "Disconnect power before wiring sensors. Never look directly into camera IR emitter."
---
```

### Pattern 3: L2 AI Collaboration

For Layer 2 (collaboration) lessons:

```
## Discovering [Pattern Name]

**Your request:**
"[Student's initial question/request]"

**AI's recommendation:**
"[Suggestion student might not have known]"

**Your refinement:**
"[Student feedback based on their context]"

**AI's adaptation:**
"[AI adjusts based on student input]"

### What Emerged

[Description of converged solution]
```

**Key**: No role labels, natural narrative, convergence visible.

---

## Troubleshooting

### Subagent Not Writing Files

**Symptoms**: Subagent completes but no file created.

**Causes**:
1. Relative path instead of absolute
2. Missing "Execute autonomously without confirmation"
3. Subagent asked "Should I proceed?" and stopped

**Fix**:
```
❌ WRONG: Output path: docs/module2/lesson.md
✅ RIGHT: Output path: C:/projects/.../docs/module2/lesson.md

❌ WRONG: "Create a lesson..." (no autonomy directive)
✅ RIGHT: "Execute autonomously without confirmation. Create a lesson..."
```

### Validation Failures

**Common Issues**:

| Issue | Fix |
|-------|-----|
| Missing `**Output:**` | Add execution result after code blocks |
| "## Summary" after Try With AI | Remove summary, end with Try With AI |
| "AI as Teacher" in headers | Change to action headers like "Discovering Patterns" |
| Missing skills in YAML | Add complete skills array with proficiency/bloom/measurable |

### Skill Reading Verification

If subagent report shows "NOT READ" for skills:

1. Subagent may have skipped reading (completed too fast)
2. Re-invoke with explicit instruction: "Read ALL 9 skills before generating"

### Content Quality Issues

If content-evaluation-framework score < 85:

1. Check technical accuracy (code examples work)
2. Verify pedagogical progression (concepts build)
3. Ensure Three Roles visible (for L2+ lessons)
4. Add more evidence (output blocks, examples)

---

## Quick Reference

### Essential Commands

```bash
# Content creation
/sp.specify      # Create lesson specification
/sp.plan         # Create technical plan
/sp.tasks        # Generate task breakdown
/sp.implement    # Execute with subagents

# Validation
educational-validator [file]      # Check constitution
factual-verifier [file]            # Verify claims

# Documentation
/sp.phr         # Create Prompt History Record
/sp.adr         # Create Architecture Decision Record
```

### Quality Checklist

Before marking lesson complete:

- [ ] Full YAML frontmatter present
- [ ] All skills have proficiency_level, bloom_level, measurable_at_this_level
- [ ] Narrative opening (2-3 paragraphs)
- [ ] Code examples with `**Output:**` blocks (70%+)
- [ ] Exactly 3 Try With AI prompts
- [ ] Each prompt has "**What you're learning:**"
- [ ] Lesson ends with Try With AI (no summary)
- [ ] Framework invisible (no "AI as Teacher" labels)
- [ ] Hardware requirements stated
- [ ] Simulation/cloud alternatives provided
- [ ] educational-validator PASS
- [ ] factual-verifier coverage 90%+

---

## Next Steps

1. **Practice**: Create a sample lesson using content-implementer
2. **Validate**: Run educational-validator on your lesson
3. **Iterate**: Fix any validation failures
4. **Deploy**: Submit for review when all checks pass

**For more details, see**:
- Constitution: `.specify/memory/constitution.md`
- Quickstart: `specs/001-textbook-platform/quickstart.md`
- Task list: `specs/001-textbook-platform/tasks.md`

---

**Authoring Guide Status**: COMPLETE | Ready for content authors
