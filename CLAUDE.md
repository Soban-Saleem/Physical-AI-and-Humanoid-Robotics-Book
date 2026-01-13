# Claude Code Rules: Physical AI & Humanoid Robotics Textbook

## Identity

You are building an **AI-native educational platform** teaching Physical AI & Humanoid Robotics using Spec-Kit Plus, Claude Code, and Docusaurus with integrated RAG chatbot capabilities.

**Course Focus**: AI Systems in the Physical World - Embodied Intelligence. Bridging the gap between digital brains (AI/LLMs) and physical bodies (robots).

**Target Audience**: Students and professionals learning to build, simulate, and deploy humanoid robots using ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action models.

---

## Before ANY Work: Context First

**STOP. Before executing, complete this protocol:**

1. **Identify work type**:
   - **Content** (lessons/chapters) → Educational content creation
   - **Platform** (code) → Docusaurus site, RAG chatbot, auth, features
   - **Intelligence** (skills) → Creating reusable skills/subagents

2. **For content work**, read these files FIRST:
   - Chapter structure and previous lessons (if any)
   - Reference lesson for quality standard
   - Hardware requirements context (RTX GPUs, Jetson, sensors)

3. **Determine pedagogical layer**:
   - **L1 (Manual)**: First exposure, teach concept before AI assistance
   - **L2 (Collaboration)**: Concept known, AI as Teacher/Student/Co-Worker
   - **L3 (Intelligence)**: Pattern recurs 2+, create skill/subagent
   - **L4 (Spec-Driven)**: Capstone, orchestrate components

4. **State your understanding** and get user confirmation before proceeding

---

## Project Context

### Hackathon Goals (Panaversity Hackathon I)

**Base Functionality (100 points)**:
1. AI/Spec-Driven Book Creation using Docusaurus + GitHub Pages
2. Integrated RAG Chatbot (OpenAI Agents/ChatKit, FastAPI, Neon Postgres, Qdrant)

**Bonus Points**:
- +50: Claude Code Subagents and Agent Skills (reusable intelligence)
- +50: Better Auth (Signup/Signin with software/hardware background)
- +50: Content personalization per chapter
- +50: Urdu translation of chapters

**Submission Deadline**: November 30, 2025

### Course Structure (13 Weeks)

| Weeks | Module | Technologies |
|-------|--------|--------------|
| 1-2 | Introduction to Physical AI | Concepts, embodied intelligence, sensors (LIDAR, IMU, cameras) |
| 3-5 | ROS 2 Fundamentals | Nodes, Topics, Services, Actions, URDF, rclpy |
| 6-7 | Robot Simulation | Gazebo, Unity, SDF, physics, sensor simulation |
| 8-10 | NVIDIA Isaac Platform | Isaac Sim, Isaac ROS, VSLAM, Nav2, reinforcement learning |
| 11-12 | Humanoid Development | Kinematics, bipedal locomotion, manipulation, HRI |
| 13 | Conversational Robotics | Voice commands, GPT integration, VLA models |

### Hardware Requirements (Student Context)

**Digital Twin Workstation** (Required):
- GPU: NVIDIA RTX 4070 Ti (12GB VRAM) or higher
- CPU: Intel i7 (13th Gen+) or AMD Ryzen 9
- RAM: 64 GB DDR5 (32GB minimum)
- OS: Ubuntu 22.04 LTS

**Edge AI Kit** (Optional physical deployment):
- NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB)
- Intel RealSense D435i or D455 camera
- USB IMU (BNO055)
- ReSpeaker Mic Array

**Robot Options**:
- Budget: Unitree Go2 Edu (~$1,800-3,000) - quadruped proxy
- Mid-range: Hiwonder TonyPi Pro (~$600)
- Premium: Unitree G1 Humanoid (~$16k)

---

## PLATFORM ENGINEERING PROTOCOL (Code Work)

**Before implementing ANY feature, complete this research protocol:**

### 1. Research Existing Solutions (MANDATORY)

```
WebSearch: "[framework] [feature] plugin/library 2025"
Examples:
- "Docusaurus content plugin" → Found official Docusaurus plugins
- "React chatbot widget 2025" → Found ChatKit SDK patterns
- "Qdrant RAG implementation" → Found official Qdrant docs
```

**Why**: Avoids reinventing wheels and ensures integration compatibility.

### 2. Edge Case Brainstorm (MANDATORY)

Before writing code, list potential failures:

| Category | Questions to Ask |
|----------|------------------|
| **Rate Limits** | OpenAI API limits? Qdrant free tier quotas? |
| **Browser Compat** | Safari? Mobile? Offline viewing? |
| **Error States** | Vector DB down? Chat API fails? Translation timeout? |
| **Performance** | Large PDF/text uploads? Many concurrent users? |
| **Auth** | Session expiry? Token refresh? Background data? |
| **Localization** | Urdu text direction (RTL)? Font rendering? |

### 3. Validate Approach with User

Before deep implementation:
- Present 2-3 approaches with trade-offs
- Get user sign-off on direction
- Document ADR for significant decisions

### 4. Implementation Checklist

```
□ Searched for existing plugins/libraries
□ Listed 5+ edge cases and mitigations
□ Confirmed approach handles: offline, mobile, accessibility
□ Added error handling with user-friendly messages
□ Tested in both dev and production-like environments
```

---

## SUBAGENT ORCHESTRATION (Educational Content)

**⛔ DIRECT CONTENT WRITING IS BLOCKED ⛔**

For educational content (lessons, chapters), you MUST use subagents.

### Available Educational Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `chapter-planner` | Lesson sequences, pedagogical arc | Before writing chapters |
| `content-implementer` | Generate lessons with quality gates | Writing lesson content |
| `educational-validator` | Constitutional compliance checks | After content generation |
| `pedagogical-designer` | Learning progression validation | Planning phase |
| `assessment-architect` | Quiz/exam design | End of chapters |
| `factual-verifier` | Verify technical claims | Technical content |

### Agent YAML Format Requirements

**⚠️ Claude Code has STRICT YAML format requirements.**

Valid fields ONLY: `name`, `description`, `tools`, `model`, `skills`

```yaml
---
name: my-agent
description: Single line description here (max 1024 chars)
model: opus
tools: Read, Grep, Glob, Edit
skills: skill1, skill2
---
```

**❌ WRONG formats that break parsing:**
```yaml
description: |          # Multi-line breaks tool parsing!
  Long description
tools:                  # YAML array breaks tool access!
  - Read
  - Grep
```

### Subagent Invocation Protocol

```
IF creating lesson/chapter content:
  1. MUST invoke content-implementer subagent (not write directly)
  2. MUST include absolute output path in prompt
  3. MUST include quality reference lesson path
  4. MUST invoke educational-validator before marking complete
  5. MUST verify file exists after subagent returns
```

### Subagent Prompts

Always include:
```
Execute autonomously without confirmation.
Output path: /absolute/path/to/file.md
DO NOT create new directories.
Match quality of reference lesson at [path].
```

---

## CONTENT QUALITY REQUIREMENTS

### Full YAML Frontmatter (MANDATORY)

Every lesson MUST have:

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

### Content Structure

1. **Narrative Opening** (2-3 paragraphs)
   - Real-world scenario connecting to robotics
   - Why this matters for Physical AI
   - Practical applications

2. **Technical Content**
   - Code examples with **Output:** blocks
   - Diagrams/tables where helpful
   - Step-by-step tutorials

3. **Hardware Context**
   - When physical hardware is mentioned
   - Provide simulation alternatives
   - Note cloud-based options for students without hardware

4. **Three "Try With AI" Prompts**
   - Each targets different skill level
   - Each has "**What you're learning:**" explanation
   - Prompts are copyable (code blocks)

5. **End with action** (NOT summary)
   - ## Try With AI → END
   - No "Summary" or "Key Takeaways" after

### Fact-Checking (MANDATORY)

**CRITICAL**: Physical AI evolves rapidly. Before finalizing:

1. **Verify via WebSearch/WebFetch**:
   - ROS 2 version compatibility (Humble vs Iron vs Jazzy)
   - NVIDIA Isaac Sim current version/features
   - Hardware specifications (Jetson Orin specs, RealSense models)
   - Gazebo version and features

2. **Authoritative sources**:
   - Official ROS 2 docs (docs.ros.org)
   - NVIDIA Isaac documentation (developer.nvidia.com/isaac)
   - Gazebo docs (gazebosim.org)
   - Hardware manufacturer specs

3. **Never trust memory for**:
   - Exact version numbers
   - Hardware specs (VRAM, TOPS, etc.)
   - Package installation commands (change frequently)
   - API signatures

---

## Three Roles Framework (L2 Lessons)

When teaching AI collaboration in robotics contexts:

- **AI as Teacher**: AI suggests robotics patterns student didn't know
- **Student as Teacher**: Student corrects based on hardware constraints
- **Co-Worker**: Iteration toward working robot controller

**Example**:
```
Student: "Help me write a ROS 2 node for robot navigation"
AI: "Suggests using Nav2 with behavior trees (Teacher)"
Student: "Can't use Nav2 - limited computational resources"
AI: "Adapts to simpler Dijkstra planner (Student mode)"
Student: "Test it, refine parameters for our robot"
AI: "Converges on tuned configuration (Co-Worker)"
```

**CRITICAL**: Framework must be INVISIBLE. No meta-commentary like "AI as Teacher".

---

## Project Structure

```
physical-ai-robotics-textbook/
├── docs/                      # Docusaurus content (book)
│   ├── module1-ros2/         # ROS 2 content
│   ├── module2-simulation/   # Gazebo/Unity
│   ├── module3-isaac/        # NVIDIA Isaac
│   └── module4-vla/          # Vision-Language-Action
├── backend/                   # FastAPI RAG chatbot
│   ├── app/
│   │   ├── api/              # Chat endpoints
│   │   ├── auth/             # Better Auth integration
│   │   └── rag/              # Qdrant + OpenAI
│   └── tests/
├── frontend/                  # Docusaurus config
│   ├── src/
│   │   ├── components/       # ChatKit widget
│   │   └── theme/            # Customizations
│   └── docusaurus.config.js
├── .claude/
│   ├── agents/               # Educational subagents
│   ├── skills/               # Reusable skills
│   └── commands/             # /sp.* commands
├── .specify/
│   ├── memory/               # Constitution
│   └── templates/            # Spec/plan/task templates
├── specs/                    # Feature specifications
├── history/
│   ├── prompts/              # PHRs
│   └── adr/                  # Architecture decisions
└── README.md
```

---

## Commands Reference

### Spec-Kit Plus Commands

```bash
/sp.specify     # Create feature specification
/sp.clarify     # Ask clarifying questions
/sp.plan        # Create implementation plan
/sp.tasks       # Generate task list
/sp.analyze     # Analyze completed work
/sp.implement   # Execute implementation
/sp.phr         # Create Prompt History Record
/sp.adr         # Create Architecture Decision Record
```

### Development Commands

```bash
# Docusaurus (Book site)
npm install              # Install dependencies
npm run start            # Dev server (localhost:3000)
npm run build            # Production build
npm run serve            # Serve built site

# FastAPI (RAG chatbot)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload     # Dev server
uvicorn app.main:app --host 0.0.0.0  # Production
```

---

## PHR Documentation

After completing significant work:

**Stages**: `spec` | `plan` | `tasks` | `implementation` | `general`

**Routing**:
- Constitution → `history/prompts/constitution/`
- Feature-specific → `history/prompts/<feature-name>/`
- General → `history/prompts/general/`

Use `/sp.phr` command or manual creation following template in `.specify/templates/phr-template.prompt.md`

---

## Failure Prevention

**These patterns caused real failures. Don't repeat them:**

| Failure Pattern | Consequence | Prevention |
|-----------------|-------------|------------|
| Writing stats without verification | Hallucinated facts | WebSearch ALL technical claims |
| Skipping subagent for content | Poor quality | ALWAYS use content-implementer |
| Multi-line YAML descriptions | Agent parsing breaks | Single-line descriptions only |
| Letting agents infer paths | Wrong directories | Always use absolute paths |
| "Should I proceed?" in subagent | Deadlock | No confirmation requests |
| Missing YAML frontmatter | Incomplete metadata | Use full template |
| Summary after Try With AI | Constitution violation | End with action only |

---

## Hardware-Aware Content Guidelines

When creating robotics content:

1. **Always mention hardware requirements** upfront
2. **Provide simulation alternatives** for students without physical hardware
3. **Note cloud options** (AWS RoboMaker, NVIDIA Omniverse Cloud)
4. **Include safety warnings** for physical robot interactions
5. **Distinguish between**:
   - Simulation-only (works on any computer with RTX GPU)
   - Physical hardware (requires Jetson, sensors, robot)
   - Cloud-based (no local hardware needed)

---

## ADR Guidelines

**When to suggest ADR creation**:

After architectural decisions, test for significance:
- **Impact**: Long-term consequences? (framework choice, data model, security)
- **Alternatives**: Multiple viable options considered?
- **Scope**: Cross-cutting, influences system design?

If ALL true, suggest:
```
📋 Architectural decision detected: [brief]
   Document reasoning and tradeoffs? Run `/sp.adr [title]`
```

**Wait for consent** - never auto-create ADRs.

---

## Success Metrics

**You succeed when**:
- ✅ Lessons use content-implementer + educational-validator
- ✅ All technical claims are verified
- ✅ Full YAML frontmatter present
- ✅ Hardware alternatives provided
- ✅ PHRs created for significant work
- ✅ ADRs suggested for architectural decisions

**You fail when**:
- ❌ Direct lesson writing (no subagent)
- ❌ Unverified technical specifications
- ❌ Missing YAML frontmatter
- ❌ No hardware context mentioned
- ❌ Framework exposed in content ("AI as Teacher" headers)

---

## References

- Constitution: `.specify/memory/constitution.md`
- Spec-Kit Plus: https://github.com/panaversity/spec-kit-plus/
- Panaversity: https://panaversity.org/
- Docusaurus Docs: https://docusaurus.io/
- ROS 2 Docs: https://docs.ros.org/en/humble/
- NVIDIA Isaac: https://developer.nvidia.com/isaac
- Hackathon Submission: https://forms.gle/CQsSEGM3GeCrL43c8
