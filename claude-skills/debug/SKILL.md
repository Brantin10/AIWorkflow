---
name: debug
description: >
  Investigates errors, bugs, and unexpected behavior. Use when asked to debug,
  fix an error, figure out why something broke, investigate a crash, trace a bug,
  find the root cause, or troubleshoot an issue.
argument-hint: "[error-message-or-file]"
allowed-tools: Read, Grep, Glob, Bash
---

# Debug Investigation

Investigate the error or issue: `$ARGUMENTS`

## Phase 1: Gather Context

1. If an error message is provided, search the codebase for the exact text
2. Read the file(s) where the error originates
3. Trace the call chain — find what calls the broken function and what it calls
4. Check recent git changes near the error location: `git log --oneline -10 -- <file>`
5. Look for related config, environment variables, or dependencies

## Phase 2: Identify Root Cause

Work through these categories:

1. **Import/Module errors** — missing dependency, wrong path, circular import
2. **Type/Schema errors** — wrong data shape, missing field, type mismatch
3. **Runtime errors** — null access, index out of bounds, division by zero
4. **Logic errors** — wrong condition, off-by-one, incorrect order of operations
5. **Environment errors** — missing env var, wrong port, file not found, permissions
6. **State errors** — stale cache, race condition, async timing

## Phase 3: Report

For each issue found:

- **Root cause:** One sentence explanation of WHY it broke
- **Location:** `file:line`
- **Evidence:** The specific code or config that's wrong
- **Fix:** Exact code change needed (show before → after)

## Rules

- Always trace to the ROOT cause, not just the symptom
- Read the actual code — don't guess based on the error message alone
- If multiple issues exist, rank by severity (fix order matters)
- Don't refactor unrelated code while debugging
- If you can't reproduce or find the cause, say so and suggest next diagnostic steps
