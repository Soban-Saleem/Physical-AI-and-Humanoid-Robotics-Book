# Feature Specification: AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

**Feature Branch**: `001-textbook-platform`
**Created**: 2025-01-13
**Status**: Draft
**Input**: AI/Spec-Driven Physical AI & Humanoid Robotics Textbook

## Overview

An interactive educational platform teaching Physical AI and Humanoid Robotics to university students and professionals. The platform combines structured course content with an AI-powered chatbot for personalized learning assistance, deployed as a static site on GitHub Pages.

**Target Audience**: University students and professionals learning Physical AI, robotics engineers, developers building embodied AI systems

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse and Learn Course Content (Priority: P1)

A student visits the platform and navigates through Module 1 (Introduction to Physical AI), reading lessons that explain core concepts through narrative explanations, code examples, and hands-on exercises.

**Why this priority**: This is the core value proposition - delivering educational content. Without this, no other features matter.

**Independent Test**: Deploy the site with 3-5 lessons in Module 1. A user can navigate from the homepage, through the module sidebar, read each lesson, complete the "Try With AI" exercises, and reach the end of the module successfully.

**Acceptance Scenarios**:

1. **Given** a visitor arrives at the homepage, **When** they click on "Module 1 - Introduction to Physical AI", **Then** they see a list of available lessons with clear titles and descriptions
2. **Given** a user is reading a lesson, **When** they reach the end, **Then** they see "Try With AI" prompts that encourage hands-on practice with clear learning objectives
3. **Given** a user completes a lesson, **When** they navigate to the next lesson, **Then** the page loads within 2 seconds and maintains their reading position context
4. **Given** a user is on any lesson page, **When** they view the page metadata, **Then** they see the lesson's skill level (CEFR), Bloom's taxonomy level, and expected duration

---

### User Story 2 - Ask AI Questions About Content (Priority: P2)

A student reading about ROS 2 topics has a specific question about how message passing works. They use the integrated chatbot to ask their question and receive a relevant answer grounded in the course material.

**Why this priority**: Enhances learning through personalized support. The platform works without it, but this transforms it from static content to an interactive learning experience.

**Independent Test**: With the RAG chatbot deployed, a user can type a question like "What is the difference between a ROS 2 topic and a service?" and receive an answer that references the actual lesson content, not generic web information.

**Acceptance Scenarios**:

1. **Given** a user is viewing any lesson page, **When** they type a question in the chat widget, **Then** they receive a response within 10 seconds that cites relevant lesson sections
2. **Given** a user asks a question unrelated to Physical AI or robotics, **When** the system processes it, **Then** the chatbot politely indicates it can only answer questions about course material
3. **Given** a user asks a follow-up question, **When** they submit it, **Then** the chatbot maintains conversation context and builds on previous responses
4. **Given** the vector database is temporarily unavailable, **When** a user asks a question, **Then** they see a friendly error message explaining the feature is temporarily unavailable

---

### User Story 3 - Sign Up and Track Learning Progress (Priority: P3)

A professional wants to track their learning journey. They create an account with their background (software/hardware experience), and the system remembers their progress through lessons.

**Why this priority**: While valuable for retention and personalization, users can derive full learning value without accounts. This is an enhancement, not core functionality.

**Independent Test**: A new visitor can click "Sign Up", complete registration (providing their technical background), log in, and see which lessons they've completed. When they return later, their progress is preserved.

**Acceptance Scenarios**:

1. **Given** a new visitor, **When** they click "Sign Up" and complete the form, **Then** they receive a confirmation and are logged in automatically
2. **Given** a logged-in user, **When** they complete a lesson (mark as done), **Then** their progress percentage updates on the module overview
3. **Given** a returning user, **When** they log back in, **Then** they see their last read lesson highlighted and overall progress restored
4. **Given** a user during signup, **When** they select their background (software vs. hardware focus), **Then** future content recommendations adapt to their experience level

---

### User Story 4 - Authors Create Spec-Driven Content (Priority: P2)

An instructor or content author uses Spec-Kit Plus templates and Claude Code subagents to create new lessons with proper YAML frontmatter, learning objectives, and AI-generated exercises.

**Why this priority**: This is how the platform scales to cover all 13 modules. Without efficient content creation, the platform cannot grow beyond initial Module 1.

**Independent Test**: An author can run a command to create a new lesson, use the content-implementer subagent to generate content, run educational-validator to verify quality, and commit the lesson to the repository.

**Acceptance Scenarios**:

1. **Given** an author creates a new lesson, **When** the content-implementer subagent completes, **Then** the lesson file exists with full YAML frontmatter (skills, objectives, cognitive load)
2. **Given** a lesson is generated, **When** educational-validator runs, **Then** it returns a pass/fail status with specific feedback on constitution compliance
3. **Given** an author needs to create a skill assessment, **When** they invoke the assessment-architect subagent, **Then** they receive quiz questions aligned to the lesson's Bloom's taxonomy level
4. **Given** a lesson contains technical claims, **When** factual-verifier runs, **Then** it validates claims against authoritative sources and flags unverified assertions

---

### Edge Cases

- What happens when a user accesses the platform without JavaScript enabled? (Graceful degradation to basic content viewing)
- How does the chatbot handle questions in languages other than English? (Initial English-only, with Urdu translation as bonus feature)
- What happens when GitHub Pages deployment fails? (Clear error messaging in CI/CD logs, last successful build remains live)
- How does the system handle users without RTX GPUs for hardware requirements? (All content includes simulation alternatives and cloud-based options)
- What happens when a lesson includes code that doesn't run due to version changes? (Content verification process catches this before publication)
- How does the chatbot handle ambiguous questions? (Asks clarifying questions or provides multiple relevant contexts)
- What happens when multiple users are creating content simultaneously? (Git-based workflow handles merge conflicts normally)
- What happens when chatbot session expires (browser tab closed)? (Context cleared; user starts fresh conversation on next visit)
- What happens when OpenAI API rate limits are hit? (Queue requests for up to 30 seconds, then display friendly "service busy, please try again" message)
- What happens when Qdrant Cloud free tier storage limit (1GB) is reached? (Add alert monitoring; upgrade to paid tier or prune old embeddings when 80% capacity reached)
- What happens when anonymous (non-logged-in) users complete lessons? (No progress saved; show prompt to sign up for progress tracking on lesson completion)

## Requirements *(mandatory)*

### Functional Requirements

**Content Delivery**
- **FR-001**: Platform MUST present course content organized into modules and lessons with a navigable sidebar
- **FR-002**: Each lesson MUST display learning objectives, required hardware/software, and expected duration before the main content
- **FR-003**: Every lesson MUST include exactly three "Try With AI" exercise prompts with clear learning outcome descriptions
- **FR-004**: Lessons MUST mark hardware requirements clearly and provide simulation alternatives for users without physical hardware
- **FR-005**: Code examples MUST display expected output alongside the code
- **FR-006**: Platform MUST render mathematical equations and technical diagrams clearly

**AI Chatbot**
- **FR-007**: Chatbot MUST answer questions using information retrieved from the course content (RAG pattern)
- **FR-008**: Chatbot responses MUST cite specific lessons or sections when providing information
- **FR-009**: Chatbot MUST maintain conversation context for follow-up questions within a browser session (persists until tab/window closes using session storage)
- **FR-010**: When content doesn't contain an answer, chatbot MUST clearly state the limitation
- **FR-011**: Chatbot MUST respond to user questions within 10 seconds

**Authentication & User Management**
- **FR-012**: Users MUST be able to create accounts with email and password
- **FR-013**: Signup form MUST capture user's technical background (software/hardware experience) for content personalization
- **FR-014**: Users MUST be able to log in and log out securely
- **FR-015**: System MUST remember and display user's lesson progress across sessions (stored server-side in Neon Postgres for authenticated users only)
- **FR-016**: Users MUST be able to mark lessons as complete

**Content Creation (Spec-Kit Plus Integration)**
- **FR-017**: Authors MUST be able to generate lesson content using content-implementer subagent
- **FR-018**: Generated lessons MUST include complete YAML frontmatter with all required metadata fields
- **FR-019**: Educational-validator subagent MUST check lessons for constitution compliance
- **FR-020**: Factual-verifier subagent MUST validate technical claims against authoritative sources
- **FR-021**: Assessment-architect subagent MUST generate quiz questions aligned to Bloom's taxonomy levels

**Content Standards**
- **FR-022**: All lessons MUST follow the 4-Layer Teaching Method (L1: Manual, L2: Collaboration, L3: Intelligence, L4: Spec-Driven)
- **FR-023**: Every lesson MUST include skills metadata with CEFR proficiency level and Bloom's taxonomy classification
- **FR-024**: Technical claims MUST be verified before publication via web search of authoritative sources
- **FR-025**: Content MUST be hardware-aware, distinguishing between simulation-only and physical hardware requirements

**Deployment**
- **FR-026**: Platform MUST deploy to GitHub Pages via automated CI/CD
- **FR-027**: Site MUST be accessible via public URL without login requirements
- **FR-028**: Site MUST be mobile-responsive for viewing on tablets and phones (chatbot widget: floating button expands to bottom drawer on mobile)

### Key Entities

- **Module**: A top-level grouping of lessons covering a major topic (e.g., "Introduction to Physical AI", "ROS 2 Fundamentals"). Contains a title, description, and ordered list of lessons.

- **Lesson**: An individual learning unit with narrative content, code examples, exercises, and metadata. Key attributes include:
  - Title and description
  - Learning objectives (measurable outcomes)
  - Skills metadata (CEFR level, Bloom's taxonomy, category)
  - Hardware and software requirements
  - Duration estimate
  - Cognitive load indicators
  - Content body with "Try With AI" prompts

- **User**: A registered learner with attributes:
  - Email and authentication credentials
  - Technical background (software-focused, hardware-focused, or both)
  - Progress tracking (completed lessons, current position)
  - Session history for chatbot context

- **Chat Session**: A conversation between a user and the AI chatbot with:
  - Message history (user questions and bot responses)
  - Source citations (which lessons/sections informed the response)
  - Session timestamp and duration

- **Assessment**: Quiz or evaluation questions with:
  - Question type (MCQ, code completion, debugging, project)
  - Alignment to learning objectives
  - Bloom's taxonomy level
  - Correct answers and rubrics for open-ended questions

## Success Criteria *(mandatory)*

> **Deadline**: All success criteria (SC-001 through SC-010) must be met by November 30, 2025 (hackathon submission deadline).

### Measurable Outcomes

- **SC-001**: Visitors can navigate from homepage to any lesson in 3 or fewer clicks
- **SC-002**: Lesson pages fully load within 2 seconds on standard broadband connections
- **SC-003**: 95% of users who attempt the first of three "Try With AI" exercises in a lesson report completion in the post-lesson survey (measured via optional feedback form)
- **SC-004**: (Phase 2) In manual testing of 50 sample questions, the chatbot provides answers with source citations for at least 80% of questions
- **SC-005**: (Phase 2) Users can create accounts and complete signup in under 3 minutes
- **SC-006**: Content authors can generate a complete lesson with all required metadata in under 30 minutes using subagents
- **SC-007**: Educational-validator passes 100% of published lessons on constitution compliance checks
- **SC-008**: Every published lesson includes a "Sources" section listing URLs or references for all technical claims
- **SC-009**: Platform is accessible 24/7 via GitHub Pages with 99.9% uptime
- **SC-010**: Module 1 contains at least 4 complete lessons covering Introduction to Physical AI topics

### Constraints

**Platform Constraints**
- Static site deployment on GitHub Pages (no backend servers for content delivery)
- Content format: Markdown with YAML frontmatter
- Responsive design supporting desktop, tablet, and mobile viewports

**Timeline Constraints**
- Base functionality complete by November 30, 2025
- Module 1 content must be written and validated before submission

**Content Constraints**
- All educational content MUST use content-implementer subagent (no direct writing)
- Every lesson MUST have complete YAML frontmatter before publication
- Hardware requirements must be specified for each lesson
- Simulation alternatives must be provided for hardware-dependent content

**Technical Constraints**
- Chatbot backend uses FastAPI for API endpoints
- Vector storage uses Qdrant for semantic search
- AI responses powered by OpenAI's API
- Authentication uses Better Auth for signup/signin

## Out of Scope

The following features are explicitly NOT part of this phase:

- Mobile native applications (mobile-responsive web only)
- Full learning management system features (grading, certificates, instructor dashboards)
- Peer-to-peer collaboration features (forums, chat between users)
- Video hosting (videos will be embedded from external platforms like YouTube)
- Payment processing or course sales functionality
- Physical robot hardware provision or rental
- Multi-language support (Urdu translation planned as separate bonus feature)
- Advanced analytics or learning outcome tracking beyond basic progress
- Content versioning or A/B testing
- Offline access capability

## Dependencies & Assumptions

**Dependencies**
- GitHub repository with GitHub Pages enabled
- OpenAI API account with sufficient rate limits for chatbot
- Qdrant Cloud free tier (1GB storage, managed service)
- Neon Postgres for user progress and authentication data
- Domain name configuration (optional, defaults to github.io domain)

**Assumptions**
- Students have access to computers with web browsers
- Target audience has basic technical literacy (can install software, use command line)
- Simulation tools (Gazebo, ROS 2) can run on student machines or cloud environments
- Authors have access to Claude Code for content generation
- Initial content focuses on Module 1; expansion to 12 additional modules in future phases

## Clarifications

### Session 2025-01-13

- Q: What defines a "session" for chatbot conversation context persistence? → A: Browser session storage - context persists until browser tab/window closes
- Q: What happens when OpenAI API rate limits are hit? → A: Queue with timeout - wait up to 30 seconds, then show friendly "service busy" message
- Q: Qdrant hosting approach (cloud vs self-managed)? → A: Qdrant Cloud free tier (1GB storage, managed service)
- Q: Where is user lesson progress stored? → A: Server-side database for authenticated users only (Better Auth + Neon Postgres)
- Q: How does chatbot widget behave on mobile devices? → A: Floating button expands to bottom drawer (standard mobile chat pattern)

## Open Questions

None at this time. Specification proceeds with informed defaults for all decisions.
