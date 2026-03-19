---
name: plan
description: >
  Creates a detailed implementation plan before writing code. Use when asked to
  plan a feature, design a solution, architect a system, create a plan, think
  through an approach, or prepare for implementation.
argument-hint: "[feature-or-task]"
allowed-tools: Read, Grep, Glob
---

# Implementation Plan

Create a plan for: `$ARGUMENTS`

## Phase 1: Research

Before planning anything:

1. Read relevant files to understand the current codebase
2. Identify existing patterns, conventions, and architecture
3. Find related code that does something similar
4. Check dependencies and configuration

## Phase 2: Write Plan

Create a structured plan covering:

### Goal
One sentence: what does this achieve?

### Files to Modify
| File | Change | Why |
|------|--------|-----|
| path/to/file | Description of change | Reason |

### Files to Create
| File | Purpose |
|------|---------|
| path/to/new/file | What it does |

### Implementation Steps
Numbered steps in execution order. Each step:
- What to do (specific, not vague)
- Which file(s) to touch
- Any dependencies on previous steps

### Edge Cases
- What could go wrong?
- What inputs need special handling?
- What existing functionality could break?

### Testing
- How to verify the change works
- What to test manually
- What automated tests to add/update

## Phase 3: Review

Before presenting the plan:
- Is every step specific enough to implement without guessing?
- Are all affected files listed?
- Is the order correct (no step depends on a later step)?

## Rules

- Do NOT write any code — this is planning only
- Do NOT skip research — always read the codebase first
- Every claim about the codebase must reference a specific file
- If requirements are unclear, list your assumptions and ask the user
- Keep the plan under 100 lines — concise beats comprehensive
