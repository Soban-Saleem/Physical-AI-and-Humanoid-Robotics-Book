# Lesson Frontmatter Schema Contract

**Feature**: `001-textbook-platform` | **Version**: 1.0.0 | **Date**: 2025-01-13

## Purpose

This contract defines the required YAML frontmatter schema for all lesson content in the Physical AI & Humanoid Robotics Textbook. All lessons MUST validate against this schema before publication.

---

## Schema Definition

### Required Fields (Level 0 - Mandatory)

```yaml
---
# Navigation
sidebar_position: integer      # 1-indexed position in module sidebar
title: string                  # Lesson title (human-readable)
description: string            # SEO description (50-160 characters)
keywords: array[string]        # Search keywords (3-7 items)

# Course Structure
chapter: integer               # Module number (1-6)
lesson: integer                # Lesson number within chapter
duration_minutes: integer      # Estimated completion time

# Hardware/Software Requirements
requirements:
  hardware: string             # Required hardware specifications
  software: string             # Required software versions

# Skills Metadata (minimum 1)
skills:
  - name: string
    proficiency_level: enum    # A1 | A2 | B1 | B2 | C1 | C2
    category: enum             # Conceptual | Technical | Applied | Soft
    bloom_level: enum          # Remember | Understand | Apply | Analyze | Evaluate | Create
    measurable_at_this_level: string

# Learning Objectives (minimum 1)
learning_objectives:
  - objective: string          # Measurable outcome
    proficiency_level: enum    # A1 | A2 | B1 | B2 | C1 | C2
    bloom_level: enum          # Remember | Understand | Apply | Analyze | Evaluate | Create
    assessment_method: string  # How achievement is measured

# Cognitive Load
cognitive_load:
  new_concepts: integer        # Number of new concepts (A2: 5-7, B1: 7-10)
  assessment: string           # How learning is verified

# Differentiation
differentiation:
  extension_for_advanced: string   # For experienced students
  remedial_for_struggling: string  # Additional scaffolding
  hardware_alternatives: string    # Cloud/simulation options

# Spec Traceability
spec_id: string                # Origin spec ID (e.g., "001-textbook-platform")
requirement_ids: array[string]     # Related FR numbers

# Optional Safety Notes
safety_notes: string | null   # Warnings for physical interactions
---
```

---

## Enum Values

### Proficiency Levels (CEFR)

| Level | Description | Cognitive Load |
|-------|-------------|----------------|
| A1 | Beginner | 3-5 new concepts |
| A2 | Elementary | 5-7 new concepts |
| B1 | Intermediate | 7-10 new concepts |
| B2 | Upper Intermediate | 10-15 new concepts |
| C1 | Advanced | Unlimited (complex) |
| C2 | Mastery | Unlimited (expert) |

### Skill Categories

| Category | Description | Example Skills |
|----------|-------------|----------------|
| `Conceptual` | Understanding principles | Embodiment, sensor fusion, control theory |
| `Technical` | Implementation skills | Python, ROS 2 APIs, URDF modeling |
| `Applied` | Hands-on capabilities | Running simulations, hardware deployment |
| `Soft` | Communication/analysis | Documentation, debugging, system design |

### Bloom's Taxonomy Levels

| Level | Cognitive Process | Example Verbs |
|-------|-------------------|---------------|
| `Remember` | Recall | Define, list, identify |
| `Understand` | Explain | Describe, explain, summarize |
| `Apply` | Use | Apply, implement, demonstrate |
| `Analyze` | Break down | Analyze, compare, differentiate |
| `Evaluate` | Judge | Evaluate, assess, justify |
| `Create` | Produce | Design, create, construct |

---

## Validation Rules

### Rule 1: Completeness
All required fields must be present. Empty strings are not valid.

### Rule 2: Type Consistency
- Integers must be numeric (no quotes)
- Arrays must use YAML array syntax
- Enums must match exact values

### Rule 3: Range Constraints
- `sidebar_position`: >= 1
- `chapter`: 1-6
- `duration_minutes`: 15-180
- `new_concepts`: A2: 5-7, B1: 7-10, B2+: unlimited

### Rule 4: Spec Traceability
- `spec_id` must reference an existing spec in `specs/`
- `requirement_ids` must map to FR numbers in the referenced spec

### Rule 5: Skills-Objectives Alignment
- Each `learning_objective` should align with at least one `skill`
- `bloom_level` in objectives should match or build upon skill levels

---

## Example Valid Frontmatter

```yaml
---
sidebar_position: 1
title: "ROS 2 Topics: Publish-Subscribe Communication"
description: "Learn how ROS 2 nodes communicate asynchronously using topics and messages"
keywords: ["ros2", "topics", "publish-subscribe", "messages", "communication"]
chapter: 2
lesson: 2
duration_minutes: 75

requirements:
  hardware: "Any computer (simulation works)"
  software: "ROS 2 Humble, Ubuntu 22.04, Python 3.10"

skills:
  - name: "Understanding Publish-Subscribe Pattern"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "Explain how topics enable decoupled communication between ROS 2 nodes"
  - name: "Creating ROS 2 Publishers"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    measurable_at_this_level: "Write a Python publisher node that sends messages on a custom topic"

learning_objectives:
  - objective: "Describe the publish-subscribe communication pattern and its advantages for robotics"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Written explanation with diagram"
  - objective: "Create a working ROS 2 publisher node using Python"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Code submission producing verified output"

cognitive_load:
  new_concepts: 7
  assessment: "Student can implement a basic publisher-subscriber pair and explain message flow"

differentiation:
  extension_for_advanced: "Implement QoS settings for reliable vs. best-effort communication"
  remedial_for_struggling: "Use a fill-in-the-blank code template for the publisher structure"
  hardware_alternatives: "Cloud-based ROS 2 development environment (e.g., GitHub Codespaces)"

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-005", "FR-008"]
safety_notes: null
---
```

---

## Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `MISSING_FIELD` | Required field not present | Add the missing field |
| `INVALID_TYPE` | Wrong data type | Correct the type (string, int, array) |
| `INVALID_ENUM` | Value not in allowed set | Use exact enum value |
| `OUT_OF_RANGE` | Number outside valid range | Adjust to valid range |
| `SPEC_NOT_FOUND` | `spec_id` doesn't exist | Create spec or correct reference |
| `FR_NOT_FOUND` | `requirement_ids` doesn't exist in spec | Correct FR numbers |

---

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Schema definition | COMPLETE | This document |
| Validator script | TODO | Create educational-validator agent |
| Template generator | TODO | Add to Spec-Kit Plus templates |
| CI/CD validation | TODO | Add to GitHub Actions |

---

## References

- Data Model: `specs/001-textbook-platform/data-model.md`
- Constitution: `.specify/memory/constitution.md`
- Spec: `specs/001-textbook-platform/spec.md`
