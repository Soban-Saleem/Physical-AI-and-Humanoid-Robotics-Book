# ADR-002: Content Organization Strategy

> **Scope**: Navigation structure and content organization for 6-module, 13-week curriculum.

- **Status:** Accepted
- **Date:** 2025-01-13
- **Feature:** textbook-platform
- **Context:** Module organization for ~50 lessons across 13 weeks of Physical AI curriculum

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - affects all content, navigation, UX
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - 3 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - determines how students navigate entire course
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use single Docusaurus docs instance with category-based sidebars for module organization.**

**Organization Structure:**
```
docs/
├── intro/                 # Front matter
│   ├── about.md
│   ├── prerequisites.md
│   └── hardware-guide.md
├── module1-intro/         # Weeks 1-2: Introduction to Physical AI
├── module2-ros2/          # Weeks 3-5: ROS 2 Fundamentals
├── module3-simulation/    # Weeks 6-7: Robot Simulation
├── module4-isaac/         # Weeks 8-10: NVIDIA Isaac Platform
├── module5-humanoid/      # Weeks 11-12: Humanoid Development
├── module6-conversational/ # Week 13: Conversational Robotics
└── appendices/            # Cheat sheets, glossary, references
```

**Navigation Pattern:**
- Each module = Docusaurus category with collapsible sidebar
- Lessons within modules ordered by `sidebar_position` frontmatter
- Front matter (intro) and appendices as separate categories

## Consequences

### Positive

- **Simplest launch path** - one `docusaurus.config.js`, one `sidebars.js`
- **Unified search** - AI-powered search indexes all modules together
- **Easy content authoring** - authors work in one directory structure
- **Consistent navigation** - all modules follow same sidebar pattern
- **Lower maintenance** - single deployment, single configuration
- **Better mobile UX** - collapsible categories work well on mobile
- **Easier onboarding** - new authors learn one pattern

### Negative

- **No independent versioning** - all modules share same version
- **Coupled deployments** - any content change triggers full rebuild
- **Shared Docusaurus version** - can't run different modules on different versions
- **Harder to extract individual modules** - can't easily publish module standalone

## Alternatives Considered

### Alternative A: Multi-Instance Docusaurus Docs
**Structure:** Each module is a separate Docusaurus docs instance with independent configuration
**Why rejected:**
- More complex - 6x configurations, 6x deployments
- No need for independent versioning in Phase 1
- Harder to maintain - changes require updating multiple instances
- Search becomes fragmented or requires complex aggregation
- **Migration path exists** - can adopt later if independent module versioning becomes critical

### Alternative B: Flat Structure (No Module Grouping)
**Structure:** All 50+ lessons in single `docs/` directory with numeric prefixes
**Why rejected:**
- Poor navigation - students can't see module boundaries
- Hard to browse - overwhelming list of lessons
- No module-level context or overview
- Doesn't match mental model of 13-week course
- Difficult to maintain - naming collisions inevitable

### Alternative C: Hybrid (Categories + Numbered Lessons)
**Structure:** Categories for modules, but all lessons named `L01-title.md`, `L02-title.md` globally
**Why rejected:**
- Numbering complexity when lessons added/removed
- Ambiguous which lesson belongs to which module
- Makes reordering within modules difficult
- Categories provide grouping anyway - numbers redundant

## Migration Path

**If multi-instance becomes necessary:**
```
Current: Single instance with categories
     ↓ (if independent module versioning needed)
Future: Multi-instance docs
     ├── docs-instance-1/ (module1-intro)
     ├── docs-instance-2/ (module2-ros2)
     └── ...
```

**Migration effort:** Low - existing directory structure maps 1:1 to multi-instance pattern. Each module folder becomes a docs instance. No content changes required.

**Trigger for migration:**
- Need to version modules independently (e.g., Module 2 updated while Module 1 stable)
- Different teams owning different modules
- Module-specific deployment cadences

## Content Mapping

| Weeks | Module | Directory | Lesson Count |
|-------|--------|-----------|--------------|
| Front matter | - | `intro/` | 3 |
| 1-2 | Introduction to Physical AI | `module1-intro/` | 3-5 |
| 3-5 | ROS 2 Fundamentals | `module2-ros2/` | 5-8 |
| 6-7 | Robot Simulation | `module3-simulation/` | 4-6 |
| 8-10 | NVIDIA Isaac Platform | `module4-isaac/` | 6-8 |
| 11-12 | Humanoid Development | `module5-humanoid/` | 5-7 |
| 13 | Conversational Robotics | `module6-conversational/` | 2-3 |
| Appendices | - | `appendices/` | 4 |

**Total estimated lessons:** 40-60 lessons across all modules

## References

- Feature Spec: [spec.md](../specs/001-textbook-platform/spec.md)
- Implementation Plan: [plan.md](../specs/001-textbook-platform/plan.md)
- Data Model: [data-model.md](../specs/001-textbook-platform/data-model.md)
- Related ADRs: ADR-001 (Static Site Platform)
