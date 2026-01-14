# Data Model: AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

**Feature**: `001-textbook-platform` | **Phase**: 1 (Design) | **Date**: 2025-01-13

## Overview

This document defines the content entities and their relationships for the Physical AI & Humanoid Robotics Textbook. As a static site, data is stored as Markdown files with YAML frontmatter rather than a traditional database.

---

## Core Entities

### 1. Module

A top-level grouping of lessons covering a major topic area.

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., `module2-ros2`) |
| `title` | string | Yes | Display name (e.g., "ROS 2 Fundamentals") |
| `week_range` | string | Yes | Course weeks covered (e.g., "3-5") |
| `description` | string | Yes | Brief description of module content |
| `lessons` | array[Lesson] | Yes | Ordered list of lessons in the module |

**Relationships**:
- Contains many Lessons
- Belongs to Course

**Example**:
```yaml
# Represented as directory structure
module2-ros2/
├── 01-introduction-to-ros2.md
├── 02-nodes-and-topics.md
├── 03-services-and-actions.md
└── 04-urdf-robot-models.md
```

---

### 2. Lesson

An individual learning unit with narrative content, code examples, exercises, and metadata.

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sidebar_position` | integer | Yes | Navigation order within module |
| `title` | string | Yes | Lesson title |
| `description` | string | Yes | Brief description for SEO/cards |
| `keywords` | array[string] | Yes | Search keywords |
| `chapter` | integer | Yes | Module number (1-6) |
| `lesson` | integer | Yes | Lesson number within chapter |
| `duration_minutes` | integer | Yes | Estimated completion time |

**Hardware/Software Requirements**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `requirements.hardware` | string | Yes | Required hardware (e.g., "RTX 4070 Ti") |
| `requirements.software` | string | Yes | Required software (e.g., "ROS 2 Humble") |

**Skills Metadata**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skills` | array[Skill] | Yes | Array of skill objects |
| `skills[].name` | string | Yes | Skill name |
| `skills[].proficiency_level` | enum | Yes | A1, A2, B1, B2, C1, C2 (CEFR) |
| `skills[].category` | enum | Yes | Conceptual, Technical, Applied, Soft |
| `skills[].bloom_level` | enum | Yes | Remember, Understand, Apply, Analyze, Evaluate, Create |
| `skills[].measurable_at_this_level` | string | Yes | How skill is demonstrated |

**Learning Objectives**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `learning_objectives` | array[Objective] | Yes | Array of learning objectives |
| `learning_objectives[].objective` | string | Yes | Measurable outcome |
| `learning_objectives[].proficiency_level` | enum | Yes | Target CEFR level |
| `learning_objectives[].bloom_level` | enum | Yes | Target Bloom's level |
| `learning_objectives[].assessment_method` | string | Yes | How achievement is measured |

**Cognitive Load**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cognitive_load.new_concepts` | integer | Yes | Number of new concepts (A2: 5-7, B1: 7-10) |
| `cognitive_load.assessment` | string | Yes | How learning is verified |

**Differentiation**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `differentiation.extension_for_advanced` | string | Yes | Enhancement for experienced students |
| `differentiation.remedial_for_struggling` | string | Yes | Scaffolding for struggling students |
| `differentiation.hardware_alternatives` | string | Yes | Cloud/simulation options |

**Safety**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `safety_notes` | string | No | Warnings for physical robot interactions |

**Spec Linkage**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `spec_id` | string | Yes | Origin spec (e.g., "001-textbook-platform") |
| `requirement_ids` | array[string] | Yes | Related FRs (e.g., ["FR-001", "FR-003"]) |

**Relationships**:
- Belongs to Module
- Contains multiple Code Examples
- Contains multiple Try With AI Prompts
- May have associated Assessment

**Complete Example**:
```yaml
---
sidebar_position: 1
title: "Introduction to ROS 2"
description: "Learn the fundamentals of the Robot Operating System 2"
keywords: ["ros2", "robotics", "middleware"]
chapter: 2
lesson: 1
duration_minutes: 60

requirements:
  hardware: "Any computer (simulation)"
  software: "ROS 2 Humble, Ubuntu 22.04"

skills:
  - name: "Understanding ROS 2 Architecture"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "Explain the publish-subscribe model"

learning_objectives:
  - objective: "Describe the ROS 2 node architecture"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Written explanation with diagram"

cognitive_load:
  new_concepts: 6
  assessment: "Student can identify nodes, topics, and messages"

differentiation:
  extension_for_advanced: "Compare ROS 1 vs ROS 2 architecture"
  remedial_for_struggling: "Create a concept map of ROS 2 components"
  hardware_alternatives: "Cloud-based ROS 2 development environment"

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-005"]
safety_notes: null
---
```

---

### 3. Code Example

Executable code with expected output for verification.

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `language` | enum | Yes | python, cpp, bash, yaml, xml |
| `code` | string | Yes | The code block |
| `output` | string | Yes | Expected execution result |
| `caption` | string | No | Description of what code does |

**Validation Rules**:
- All code examples MUST have `**Output:**` block following them
- Output must be verified by execution before inclusion
- Code lines should be under 80 characters for mobile readability

**Example**:
````markdown
```python
import rclpy
from rclpy.node import Node

rclpy.init()
node = Node('minimal_node')
node.get_logger().info('Hello, Physical AI!')
```

**Output:**
```
[INFO] [minimal_node]: Hello, Physical AI!
```
````

---

### 4. Try With AI Prompt

Interactive exercise prompts for hands-on learning.

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | The exercise prompt for AI |
| `skill_level` | enum | Yes | beginner, intermediate, advanced |
| `what_youre_learning` | string | Yes | Explanation of learning outcome |
| `estimated_time` | integer | No | Minutes to complete |

**Structure Rules**:
- Each lesson MUST include exactly 3 Try With AI prompts
- Each prompt targets a different skill level
- Must include "**What you're learning:**" explanation
- Prompts must be copyable (in code blocks)

**Example**:
````markdown
### Try With AI

```text
Ask an AI to help you write a ROS 2 publisher node that sends a "Hello" message
every second. Have it explain each part of the code: the node creation, the
publisher, the timer callback, and the shutdown process.
```

**What you're learning:** ROS 2 node structure, the publish-subscribe pattern,
and how to create a minimal working example with proper lifecycle management.
````

---

### 5. Assessment (Quiz/Exam)

Evaluation questions aligned to learning objectives.

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique assessment identifier |
| `lesson_id` | string | Yes | Associated lesson |
| `questions` | array[Question] | Yes | Assessment questions |
| `passing_score` | integer | Yes | Minimum percentage to pass |

**Question Types**:
| Type | Description |
|------|-------------|
| `mcq` | Multiple choice question |
| `code_completion` | Fill in missing code |
| `debugging` | Find and fix errors |
| `project` | Open-ended project |

**Question Schema**:
```yaml
question:
  id: "q1"
  type: "mcq"
  text: "What is the primary communication pattern in ROS 2?"
  options:
    - text: "Request-Response"
      correct: false
    - text: "Publish-Subscribe"
      correct: true
    - text: "Direct Method Call"
      correct: false
  bloom_level: "Remember"
  points: 1
```

---

### 6. User (Authentication - Future Phase)

Registered learner with progress tracking (P3 priority - not in initial MVP).

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique user identifier |
| `email` | string | Yes | User email (auth credential) |
| `technical_background` | enum | Yes | software, hardware, both |
| `created_at` | datetime | Yes | Account creation timestamp |
| `progress` | Progress | No | Lesson completion tracking |

**Progress Schema**:
```yaml
progress:
  completed_lessons: ["module2-ros2/01-introduction", ...]
  current_lesson: "module2-ros2/02-nodes-topics"
  last_position: "2025-01-13T10:30:00Z"
  completion_percentage: 23
```

---

### 7. Chat Session (RAG Chatbot - Future Phase)

Conversation between user and AI chatbot (P2 priority).

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique session identifier |
| `user_id` | string | No | User ID (null for anonymous) |
| `messages` | array[Message] | Yes | Conversation history |
| `created_at` | datetime | Yes | Session start |
| `expires_at` | datetime | Yes | Session expiration (browser close) |

**Message Schema**:
```yaml
message:
  role: "user" | "assistant"
  content: string
  citations: array[string]  # Lesson references
  timestamp: datetime
```

---

## Entity Relationships

```
Course
├── Front Matter (intro/)
│   ├── about.md
│   ├── prerequisites.md
│   └── hardware-guide.md
├── Module 1: Introduction (module1-intro/)
│   ├── Lesson 1
│   ├── Lesson 2
│   └── Lesson 3
├── Module 2: ROS 2 (module2-ros2/)
│   ├── Lesson 1 → has 3 Code Examples, 3 Try With AI Prompts
│   ├── Lesson 2 → has Assessment
│   └── Lesson 3
├── Module 3: Simulation (module3-simulation/)
├── Module 4: Isaac (module4-isaac/)
├── Module 5: Humanoid (module5-humanoid/)
├── Module 6: Conversational (module6-conversational/)
└── Appendices (appendices/)
    ├── ros2-cheat-sheet.md
    ├── troubleshooting.md
    └── references.md
```

---

## Validation Rules

### YAML Frontmatter Completeness

Every lesson MUST have:
- [ ] `sidebar_position` (1-indexed)
- [ ] `title` and `description`
- [ ] `keywords` array
- [ ] `chapter` and `lesson` numbers
- [ ] `duration_minutes`
- [ ] `requirements.hardware` and `requirements.software`
- [ ] At least one skill with all 5 fields
- [ ] At least one learning objective
- [ ] `cognitive_load.new_concepts` and `cognitive_load.assessment`
- [ ] All three `differentiation` fields
- [ ] `spec_id` and `requirement_ids`

### Content Structure

Every lesson MUST contain:
- [ ] Narrative opening (2-3 paragraphs)
- [ ] At least one code example with output
- [ ] Exactly three "Try With AI" prompts
- [ ] End with `## Try With AI` (no summary after)

### Spec Traceability

- [ ] `spec_id` references existing spec in `specs/`
- [ ] `requirement_ids` map to FR numbers in spec

---

## State Transitions

### Lesson Lifecycle

```
Draft → In Review → Validated → Published
         ↓            ↓
       Rejected    Revisions Needed
```

| State | Description | Entry Criteria |
|-------|-------------|----------------|
| `Draft` | Initial content generation | Content-implementer creates file |
| `In Review` | Ready for validation | Author submits for review |
| `Validated` | Passes all checks | Educational-validator returns PASS |
| `Published` | Live on GitHub Pages | Merged to master branch |
| `Rejected` | Fails validation | Educational-validator returns FAIL |
| `Revisions Needed` | Minor issues | Validator feedback provided |

---

## File System Schema

```
docs/
├── intro/
│   ├── _category_.yml          # Module metadata
│   ├── about.md
│   ├── prerequisites.md
│   └── hardware-guide.md
├── module1-intro/
│   ├── _category_.yml
│   ├── 01-what-is-physical-ai.md
│   ├── 02-sensors-actuators.md
│   └── 03-embodiment-gap.md
├── module2-ros2/
│   ├── _category_.yml
│   ├── 01-introduction.md
│   ├── 02-nodes-topics.md
│   ├── 03-services-actions.md
│   └── 04-urdf-models.md
├── module3-simulation/
├── module4-isaac/
├── module5-humanoid/
├── module6-conversational/
└── appendices/
    ├── _category_.yml
    ├── ros2-cheat-sheet.md
    ├── troubleshooting.md
    ├── glossary.md
    └── references.md
```

**`_category_.yml` Schema**:
```yaml
label: Module Title
collapsible: true
collapsed: false
link:
  type: generated-index
  title: Module Overview
```

---

**Data Model Status**: COMPLETE | Ready for Phase 1 contract generation
