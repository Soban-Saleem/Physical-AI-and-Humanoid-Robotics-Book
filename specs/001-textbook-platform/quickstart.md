# Quickstart Guide: AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

**Feature**: `001-textbook-platform` | **Version**: 1.0.0 | **Date**: 2025-01-13

## Overview

This guide helps content authors and contributors get started with creating lessons for the Physical AI & Humanoid Robotics Textbook using Spec-Kit Plus, Claude Code, and Docusaurus.

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Node.js | 20.x LTS | Docusaurus site generator |
| npm | 10.x | Package management |
| Git | Latest | Version control |
| Claude Code | Latest | AI-assisted development |
| Python | 3.10+ | Content validation scripts (optional) |

### Required Accounts

- **GitHub**: For repository access and GitHub Pages deployment
- **Claude API**: For Claude Code subagent usage

### Recommended Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32 GB |
| Storage | 10 GB SSD | 50 GB SSD |
| GPU | None | RTX 4070 Ti (for Isaac Sim content) |

---

## Initial Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_ORG/physical-ai-robotics-textbook.git
cd physical-ai-robotics-textbook
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Start Development Server

```bash
npm run start
```

Visit `http://localhost:3000` to see the site.

---

## Content Creation Workflow

### Overview

```
1. /sp.specify → Create feature specification
2. /sp.plan    → Create technical plan
3. /sp.tasks   → Generate task breakdown
4. /sp.implement → Execute implementation (uses subagents)
5. Validate    → Educational-validator checks quality
6. Deploy      → Merge to master, auto-deploys to GitHub Pages
```

---

## Creating a New Lesson

### Step 1: Create Specification

```bash
/sp.specify
```

**Prompt Template**:
```
Create a lesson on [TOPIC] for Module [X].
Target audience: [students/professionals]
Prerequisites: [previous lessons/concepts]
Learning objectives: [what students will achieve]
```

**Output**: `specs/###-lesson-name/spec.md`

---

### Step 2: Create Technical Plan

```bash
/sp.plan
```

**Prompt Template**:
```
Using Docusaurus with YAML frontmatter following the constitution.
Include: code examples, hardware requirements, 3 Try With AI prompts.
Hardware: [simulation-only / physical hardware required]
```

**Output**: `specs/###-lesson-name/plan.md`

---

### Step 3: Generate Tasks

```bash
/sp.tasks
```

**Output**: `specs/###-lesson-name/tasks.md`

---

### Step 4: Implement Content

```bash
/sp.implement
```

This invokes the **content-implementer** subagent which:
1. Reads 9 required skills (blocking, 30-60 seconds)
2. Reads reference lesson and constitution
3. Generates content with full YAML frontmatter
4. Self-scores with content-evaluation-framework
5. Writes file directly to `docs/module-X/`

**Critical**: Always provide absolute output path:
```
Output path: /absolute/path/to/physical-ai-robotics-textbook/docs/module2-ros2/01-lesson-name.md
Reference lesson: docs/module1-intro/01-what-is-physical-ai.md
```

---

### Step 5: Validate Content

The educational-validator runs automatically to check:
- ✅ Framework invisibility (no role labels)
- ✅ Evidence presence (70%+ code blocks have Output)
- ✅ Structural compliance (ends with Try With AI)
- ✅ Proficiency alignment (cognitive load matches CEFR)

If validation fails, fix issues and re-run.

---

## Lesson Template

### Complete Frontmatter

```yaml
---
sidebar_position: 1
title: "Lesson Title"
description: "Brief description for SEO"
keywords: ["keyword1", "keyword2", "keyword3"]
chapter: 1
lesson: 1
duration_minutes: 60

requirements:
  hardware: "Any computer (simulation)"
  software: "ROS 2 Humble, Ubuntu 22.04"

skills:
  - name: "Skill Name"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Understand"
    measurable_at_this_level: "How skill is demonstrated"

learning_objectives:
  - objective: "Measurable outcome"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "How achievement is measured"

cognitive_load:
  new_concepts: 6
  assessment: "How learning is verified"

differentiation:
  extension_for_advanced: "For experienced students"
  remedial_for_struggling: "Additional scaffolding"
  hardware_alternatives: "Cloud simulation options"

spec_id: "001-textbook-platform"
requirement_ids: ["FR-001", "FR-003"]
safety_notes: null
---
```

### Content Structure

```markdown
[Narrative Opening - 2-3 paragraphs connecting to real-world robotics]

## Technical Content

[Explanation with code examples and Output: blocks]

## Hardware Requirements

[Requirements statement with simulation/cloud alternatives]

## Try With AI

### Exercise 1: [Title]

\`\`\`text
[Copyable prompt]
\`\`\`

**What you're learning:** [Explanation]

### Exercise 2: [Title]

\`\`\`text
[Copyable prompt]
\`\`\`

**What you're learning:** [Explanation]

### Exercise 3: [Title]

\`\`\`text
[Copyable prompt]
\`\`\`

**What you're learning:** [Explanation]
```

---

## Common Commands

### Docusaurus Development

```bash
npm run start      # Start dev server (localhost:3000)
npm run build      # Production build
npm run serve      # Serve built site locally
npm run deploy     # Deploy to GitHub Pages
```

### Spec-Kit Plus Commands

```bash
/sp.specify        # Create feature specification
/sp.plan           # Create technical plan
/sp.tasks          # Generate task breakdown
/sp.implement      # Execute implementation
/sp.clarify        # Resolve ambiguities
/sp.phr            # Create Prompt History Record
/sp.adr            # Create Architecture Decision Record
```

### Git Workflow

```bash
git checkout -b 001-feature-name    # Create feature branch
git add .                           # Stage changes
git commit -m "feat: add lesson X"  # Commit
git push origin 001-feature-name    # Push to remote
```

---

## Quality Checklist

Before submitting a lesson for review:

### Frontmatter
- [ ] All required fields present
- [ ] `spec_id` references existing spec
- [ ] `requirement_ids` map to spec FRs
- [ ] CEFR level matches cognitive load

### Content
- [ ] Narrative opening (2-3 paragraphs)
- [ ] At least one code example with **Output:**
- [ ] Hardware requirements stated
- [ ] Simulation alternatives provided

### Structure
- [ ] Exactly 3 Try With AI prompts
- [ ] Each prompt has "**What you're learning:**"
- [ ] Lesson ends with Try With AI (no summary)

### Framework
- [ ] No "AI as Teacher" labels visible
- [ ] Framework is invisible to students

---

## Troubleshooting

### Site Won't Build

```bash
# Clear cache and rebuild
rm -rf node_modules build
npm install
npm run build
```

### Lesson Not Appearing in Sidebar

Check `sidebars.js` - ensure lesson path is included:

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Module 2: ROS 2 Fundamentals',
      items: [
        'module2-ros2/01-lesson-name',  // Check this path
      ],
    },
  ],
};
```

### Validation Failing

Common issues:
- Missing `**Output:**` after code blocks
- Summary section after Try With AI
- Framework labels in headers
- Missing skills or learning objectives

### Subagent Not Writing Files

Check:
1. Absolute path provided (not relative)
2. "Execute autonomously without confirmation" in prompt
3. No "Should I proceed?" in subagent prompt

---

## Module Structure Reference

```
docs/
├── intro/                    # Front matter
│   ├── about.md
│   ├── prerequisites.md
│   └── hardware-guide.md
│
├── module1-intro/            # Weeks 1-2: Introduction to Physical AI
│   ├── 01-what-is-physical-ai.md
│   ├── 02-sensors-and-actuators.md
│   └── 03-the-embodiment-gap.md
│
├── module2-ros2/             # Weeks 3-5: ROS 2 Fundamentals
│   ├── 01-introduction-to-ros2.md
│   ├── 02-nodes-and-topics.md
│   ├── 03-services-and-actions.md
│   └── 04-urdf-and-robot-models.md
│
├── module3-simulation/       # Weeks 6-7: Robot Simulation
├── module4-isaac/            # Weeks 8-10: NVIDIA Isaac Platform
├── module5-humanoid/         # Weeks 11-12: Humanoid Development
├── module6-conversational/   # Week 13: Conversational Robotics
│
└── appendices/               # Reference materials
    ├── ros2-cheat-sheet.md
    ├── troubleshooting.md
    ├── glossary.md
    └── references.md
```

---

## Next Steps

1. **Read the Constitution**: `.specify/memory/constitution.md`
2. **Review Sample Lesson**: `docs/module1-intro/01-what-is-physical-ai.md`
3. **Create Your First Spec**: Run `/sp.specify`
4. **Generate Content**: Use `/sp.implement` with content-implementer subagent

---

## Support

- **Constitution**: `.specify/memory/constitution.md`
- **Spec Template**: `.specify/templates/spec-template.md`
- **Data Model**: `specs/001-textbook-platform/data-model.md`
- **Contracts**: `specs/001-textbook-platform/contracts/`

---

**Quickstart Guide Status**: COMPLETE | Ready for content authors
