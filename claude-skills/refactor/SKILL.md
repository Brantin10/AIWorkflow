---
name: refactor
description: >
  Refactors code to improve structure, readability, and maintainability without
  changing behavior. Use when asked to refactor, clean up code, simplify, reduce
  duplication, extract functions, reorganize, or improve code structure.
argument-hint: "[file-or-directory]"
allowed-tools: Read, Grep, Glob
---

# Code Refactor

Refactor the code at `$ARGUMENTS`.

## Phase 1: Analysis

Read the target file(s) and identify:

1. **Long functions** — over 40 lines, candidates for extraction
2. **Duplication** — repeated logic that can be shared
3. **Deep nesting** — 3+ levels of if/for/try that can be flattened
4. **Unclear naming** — variables/functions that don't describe their purpose
5. **Mixed concerns** — functions doing multiple unrelated things
6. **Dead code** — unused imports, unreachable branches, commented-out blocks

## Phase 2: Plan Changes

For each refactor, describe:

- **What:** The specific change
- **Why:** What improves (readability, reusability, testability)
- **Risk:** Could this break anything? (LOW / MEDIUM / HIGH)
- **Before:** Current code snippet
- **After:** Proposed code snippet

## Phase 3: Implement

Apply changes one at a time. After each change:
- Verify no behavior change
- Verify types still pass (if TypeScript/Python typed)

## Rules

- NEVER change behavior — refactoring is structural only
- NEVER add new features, fix bugs, or change logic during refactoring
- Keep changes small and reviewable
- Preserve all existing tests — they must still pass
- If a refactor is risky, flag it and ask the user before proceeding
- Maximum 5 refactoring changes per invocation — don't over-refactor
