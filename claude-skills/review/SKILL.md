---
name: review
description: >
  Reviews code for bugs, security issues, performance problems, and style.
  Use when asked to review code, check code quality, audit a file, find bugs,
  look for issues, inspect code, or do a code review.
argument-hint: "[file-or-directory]"
allowed-tools: Read, Grep, Glob
---

# Code Review

Review the file or directory at `$ARGUMENTS`.

## Checklist

Check each category. Only report actual issues found.

1. **Bugs** — Logic errors, off-by-one, null/undefined risks, race conditions, missing error handling
2. **Security** — Injection, hardcoded secrets, unvalidated input, XSS, exposed API keys
3. **Performance** — Unnecessary re-renders, missing memoization, N+1 queries, large bundle imports
4. **Types** — Missing TypeScript types, `any` usage, incorrect type assertions
5. **Readability** — Unclear naming, deep nesting, functions over 50 lines, magic numbers

## Output Format

For each issue:

- **File:** `filename:line`
- **Severity:** HIGH / MEDIUM / LOW
- **Issue:** One sentence, max 20 words
- **Fix:** One sentence, max 20 words

## Summary

End with exactly:
```
Issues: X total (Y high, Z medium, W low)
Quality: N/10
```

## Rules

- Do not explain your reasoning
- Do not add introductions or conclusions beyond the summary
- Do not suggest adding new dependencies
- Do not comment on business logic correctness
- If no issues found, say "No issues found. Quality: N/10"
