---
name: review-pr
description: >
  Reviews a pull request or branch diff like a senior engineer. Analyzes all changed files for bugs,
  security vulnerabilities, performance issues, and code quality. Use when asked to review a PR,
  review branch changes, check a pull request, audit a diff, or do a PR review.
argument-hint: "[PR-number-or-branch-name]"
allowed-tools: Bash, Read, Grep, Glob
---

# Pull Request Review

Act as a senior engineer reviewing a production PR. Be concise, actionable, and direct.

## Step 1 — Gather the Diff

Determine what to review based on `$ARGUMENTS`:

- **If a PR number** (e.g. `123`): Run `gh pr diff $ARGUMENTS` and `gh pr view $ARGUMENTS` to get the diff and PR description.
- **If a branch name** (e.g. `feature/auth`): Run `git diff main...$ARGUMENTS` (or `master...$ARGUMENTS` based on the repo's default branch).
- **If empty / no argument**: Run `git diff main...HEAD` to review the current branch against main/master. Also run `git log main..HEAD --oneline` to see commits.

Also run `git diff --stat` (with the same range) to get a file-level summary of what changed and how many lines.

## Step 2 — Read Changed Files

For each changed file in the diff:
1. Read the FULL current version of the file (not just the diff hunks) to understand context
2. Note the specific lines that were added/modified/deleted from the diff

Do NOT skip files. Review everything that changed.

## Step 3 — Analyze

Check each changed file against ALL of these categories:

### Bugs & Logic Errors
- Off-by-one errors, null/undefined risks, missing edge cases
- Race conditions, async/await misuse, unhandled promise rejections
- Wrong comparisons (`==` vs `===`), incorrect type coercions
- Missing error handling, uncaught exceptions
- State mutations, stale closures, incorrect dependency arrays

### Security Vulnerabilities
- SQL/NoSQL injection, command injection, XSS, CSRF
- Hardcoded secrets, API keys, tokens in code
- Unvalidated user input, missing sanitization
- Insecure auth patterns, broken access control
- Exposed sensitive data in logs, error messages, URLs
- Unsafe deserialization, prototype pollution

### Performance Issues
- Unnecessary re-renders, missing React.memo/useMemo/useCallback
- N+1 queries, missing database indexes, unoptimized queries
- Large bundle imports (import entire library vs specific module)
- Missing pagination, unbounded data fetches
- Expensive operations in hot paths, missing caching
- Memory leaks (event listeners, intervals, subscriptions not cleaned up)

### Code Quality & Best Practices
- Unclear naming, magic numbers, deep nesting
- Functions over 50 lines, god objects, tight coupling
- Missing TypeScript types, `any` usage, incorrect assertions
- Dead code, unused imports, commented-out code
- Inconsistent patterns vs rest of codebase
- Missing input validation at system boundaries

### Breaking Changes & Risks
- API contract changes (request/response shape, status codes)
- Database schema changes without migration
- Removed or renamed exports that other code may depend on
- Changed default behavior that could surprise users
- Missing backwards compatibility handling

## Step 4 — Output the Report

Use this EXACT format:

```
## PR Review: [brief title of what the PR does]

**Files changed:** X files (+Y/-Z lines)
**Risk level:** LOW / MEDIUM / HIGH / CRITICAL

---

### Critical Issues
> Issues that MUST be fixed before merge. Bugs, data loss risks, security holes.

- **`file:line`** — [Description of issue]
  ```suggestion
  // Suggested fix (if applicable)
  ```

*(If none: "None found.")*

### Security Issues
> Vulnerabilities, exposed secrets, injection risks.

- **`file:line`** — [Description]

*(If none: "None found.")*

### Performance Improvements
> Optimizations that would meaningfully improve speed, memory, or bundle size.

- **`file:line`** — [Description + suggestion]

*(If none: "None found.")*

### Code Quality
> Style, readability, best practices, refactoring opportunities.

- **`file:line`** — [Description + suggestion]

*(If none: "Looks clean.")*

### Breaking Changes
> Changes that could affect other parts of the system or consumers.

- [Description of what changed and what might break]

*(If none: "No breaking changes detected.")*

---

### Summary

| Category | Count |
|----------|-------|
| Critical | X |
| Security | X |
| Performance | X |
| Quality | X |
| Breaking | X |

**Verdict:** APPROVE / REQUEST CHANGES / NEEDS DISCUSSION

[1-3 sentence summary of the overall PR quality and what needs attention]
```

## Rules

- Review ALL changed files, not a sample
- Only report issues in CHANGED code — don't review unchanged lines
- Be specific: always include `file:line` references
- Provide code suggestions for critical and security issues
- Don't nitpick formatting if the project has a formatter (prettier, eslint)
- Don't suggest adding new dependencies
- Don't comment on business logic correctness unless it's clearly wrong
- If the PR is clean, say so — don't invent issues
- Keep each issue description to 1-2 sentences max
- Verdict: APPROVE if no critical/security issues, REQUEST CHANGES if there are
