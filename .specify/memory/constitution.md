<!--
Sync Impact Report:
- Version change: (initial) → 1.0.0
- Modified principles: N/A (initial creation)
- Added sections: All sections (I. Spec-Driven Development, II. Educational Quality, III. Technical Accuracy, IV. Hardware-Awareness, V. Subagent Orchestration)
- Removed sections: None
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md (Constitution Check section aligned)
  ✅ .specify/templates/spec-template.md (aligned with success criteria)
  ✅ .specify/templates/tasks-template.md (aligned with subagent requirements)
  ✅ CLAUDE.md (updated with constitution references)
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All content creation MUST follow the Spec-Kit Plus workflow: Specification → Plan → Tasks → Implementation.

**Rules**:
- Every module/chapter starts with `/sp.specify` to create feature specification
- Use `/sp.plan` for architectural decisions before implementation
- Use `/sp.tasks` to break down work into testable units
- No content written without a corresponding spec/plan

**Rationale**: Spec-driven development prevents scope creep, ensures traceability, and enables parallel development of the 13-week curriculum.

### II. Educational Quality (CONSTITUTIONAL COMPLIANCE)

All educational content MUST comply with the Four Constitutional Checks: Framework Invisibility, Evidence Presence, Structural Compliance, and Proficiency Alignment.

**Rules**:
- Framework Invisibility: NO meta-commentary like "Part 2: AI as Teacher" or "AI's Role:". Use action-focused headers.
- Evidence Presence: ALL code blocks MUST have `**Output:**` showing execution results. No unverified claims.
- Structural Compliance: Lessons MUST end with `## Try With AI`. NO "Summary" or "Key Takeaways" after.
- Proficiency Alignment: Cognitive load MUST match declared CEFR level (A2: 5-7 concepts, B1: 7-10, C2: unlimited)

**Rationale**: These standards emerged from analyzing quality failures in educational content production. Students EXPERIENCE learning without seeing pedagogical scaffolding.

### III. Technical Accuracy (PRIMARY SOURCE VERIFICATION)

All technical claims MUST be verified against authoritative sources before publication.

**Verification Requirements**:
- ROS 2: Verify against docs.ros.org (Humble, Iron, Jazzy compatibility)
- NVIDIA Isaac: Verify against developer.nvidia.com/isaac
- Hardware specs: Verify against manufacturer datasheets (Jetson TOPS, RealSense specs, GPU VRAM)
- Gazebo/Unity: Check current version compatibility
- Package installations: Test commands, never assume from memory

**Never Trust Memory For**:
- Exact version numbers (ROS 2 Humble vs Iron vs Jazzy)
- Hardware specifications (RTX 4070 Ti VRAM, Jetson Orin TOPS)
- API signatures or command syntax
- Installation commands (change frequently)

**Rationale**: Physical AI evolves rapidly. Hallucinated specs create broken student experiences and erode trust.

### IV. Hardware-Awareness (ALWAYS PROVIDE ALTERNATIVES)

All content MUST acknowledge hardware diversity and provide alternatives for students without physical hardware.

**Rules**:
- Specify hardware requirements upfront (GPU, Jetson, sensors)
- Provide simulation alternatives (Gazebo, Isaac Sim)
- Note cloud-based options (AWS RoboMaker, NVIDIA Omniverse Cloud)
- Include safety warnings for physical robot interactions
- Distinguish between: Simulation-only, Physical hardware required, Cloud-based

**Rationale**: Not all students have $3,000+ for robot hardware. Alternatives ensure accessibility while maintaining learning outcomes.

### V. Subagent Orchestration (EDUCATIONAL CONTENT ONLY)

**Educational content MUST use subagents. Direct writing is BLOCKED.**

**Required Workflow**:
1. Use `chapter-planner` agent to design lesson sequences
2. Use `content-implementer` agent to generate lesson content
3. Use `educational-validator` agent to validate constitutional compliance
4. Use `factual-verifier` agent for technical claims
5. Verify file exists after subagent completion

**Subagent Prompts MUST Include**:
- Absolute output path (never relative)
- Quality reference lesson path
- "Execute autonomously without confirmation"

**Rationale**: Direct writing bypasses quality gates and caused 50% session waste in Chapter 2 incident.

## Content Standards

### YAML Frontmatter Requirements

Every lesson MUST include complete frontmatter:

```yaml
---
sidebar_position: X
title: "Lesson Title"
description: "Brief description"
keywords: ["keyword1", "keyword2"]
chapter: X
lesson: X
duration_minutes: X

# Hardware/Software Requirements
requirements:
  hardware: "RTX GPU, Jetson, etc."
  software: "ROS 2 Humble, Gazebo, etc."

# Skills Metadata
skills:
  - name: "Skill Name"
    proficiency_level: "A1|A2|B1|B2|C1|C2"
    category: "Conceptual|Technical|Applied|Soft"
    bloom_level: "Remember|Understand|Apply|Analyze|Evaluate|Create"
    measurable_at_this_level: "How skill is demonstrated"

learning_objectives:
  - objective: "Measurable outcome"
    proficiency_level: "..."
    bloom_level: "..."
    assessment_method: "..."

cognitive_load:
  new_concepts: X
  assessment: "How learning is verified"

differentiation:
  extension_for_advanced: "For students with prior experience"
  remedial_for_struggling: "Additional scaffolding"
  hardware_alternatives: "Cloud simulation options"

safety_notes: "If applicable (robot hardware, high voltage, etc.)"
---
```

### Content Structure Requirements

1. **Narrative Opening** (2-3 paragraphs)
   - Real-world robotics scenario
   - Connection to Physical AI goals
   - Practical applications

2. **Technical Content**
   - Code examples with `**Output:**` blocks
   - Diagrams/tables for complex concepts
   - Step-by-step tutorials

3. **Hardware Context**
   - Requirements stated upfront
   - Simulation alternatives provided
   - Cloud options noted

4. **Three "Try With AI" Prompts**
   - Each targets different skill level
   - Each has "**What you're learning:**" explanation
   - Prompts are copyable (code blocks)

5. **End with Action**
   - `## Try With AI` → END
   - NO "Summary" after
   - NO "Key Takeaways" after

## Three Roles Framework (L2 Lessons)

When teaching AI collaboration in robotics:

- **AI as Teacher**: AI suggests robotics patterns student didn't know
- **Student as Teacher**: Student corrects based on hardware constraints
- **Co-Worker**: Iteration toward working solution

**Example**:
```
Student: "Help me write a ROS 2 node for robot navigation"
AI: "Suggests using Nav2 with behavior trees (Teacher)"
Student: "Can't use Nav2 - limited computational resources"
AI: "Adapts to simpler Dijkstra planner (Student mode)"
Student: "Test it, refine parameters for our robot"
AI: "Converges on tuned configuration (Co-Worker)"
```

**CRITICAL**: Framework must be INVISIBLE. No meta-commentary like "AI as Teacher" in student-facing content.

## Technology Stack

### Content Platform
- **Docusaurus**: Static site generator for book content
- **GitHub Pages**: Deployment target
- **Markdown**: Content format with YAML frontmatter

### Development Tools
- **Spec-Kit Plus**: Spec-driven development workflow
- **Claude Code**: AI-assisted development and subagent orchestration

### Educational Subagents
- `chapter-planner`: Lesson sequence design
- `content-implementer`: Content generation with quality gates
- `educational-validator`: Constitutional compliance checks
- `factual-verifier`: Technical claim verification
- `assessment-architect`: Quiz/exam design

### Course Technologies (Content)
- **ROS 2**: Robot Operating System (Humble, Iron, Jazzy)
- **Gazebo**: Physics simulation
- **Unity**: High-fidelity rendering
- **NVIDIA Isaac**: Isaac Sim, Isaac ROS, VSLAM, Nav2
- **VLA Models**: Vision-Language-Action integration

## Constraints

### Word Count
- Lessons: 1,500-3,000 words per lesson
- Modules: 6 modules total (13 weeks) per ADR-002
- Total book: ~50,000 words estimated

### Proficiency Progression
- Weeks 1-2: A2 (Foundational)
- Weeks 3-7: B1 (Intermediate)
- Weeks 8-13: B2/C1 (Advanced)

### Platform Constraints
- Must deploy to GitHub Pages (static hosting)
- Must work offline after initial load
- Mobile-responsive reading experience

## Success Criteria

### Content Quality
- All lessons pass `educational-validator` checks
- Zero hallucinated technical specifications
- All code examples have verified output
- Full YAML frontmatter on every lesson

### Accessibility
- Hardware alternatives provided for all physical exercises
- Cloud simulation options noted where applicable
- Safety warnings for hardware interactions

### Completeness
- All 4 modules published to GitHub Pages
- 13-week curriculum fully specified
- Each module has: spec → plan → tasks → implementation
- PHR documentation for all significant work

## Governance

### Amendment Process
1. Propose amendment via issue or discussion
2. Document rationale and impact
3. Update version number (semantic versioning)
4. Propagate changes to dependent templates
5. Create PHR documenting the change

### Versioning
- **MAJOR**: Backward incompatible principle changes
- **MINOR**: New principles added or material expansions
- **PATCH**: Clarifications and wording improvements

### Compliance Review
- All content MUST pass `educational-validator` before publication
- All technical claims MUST pass `factual-verifier`
- Constitution violations block deployment

### Reference Documents
- CLAUDE.md: Runtime development guidance
- `.claude/agents/`: Subagent definitions
- `.specify/templates/`: Plan/spec/task templates

---

**Version**: 1.0.0 | **Ratified**: 2025-01-13 | **Last Amended**: 2025-01-13
