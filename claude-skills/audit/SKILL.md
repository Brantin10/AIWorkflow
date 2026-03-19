---
name: audit
description: >
  Security audit of code. Use when asked to check for vulnerabilities, security issues,
  hardcoded secrets, API keys, passwords, injection risks, or scan for security problems.
argument-hint: "[file-or-directory]"
allowed-tools: Read, Grep, Glob
---

# Security Audit

Audit `$ARGUMENTS` for security vulnerabilities.

## Scan For

1. **Hardcoded secrets** — API keys, passwords, tokens, connection strings, private keys
2. **Env exposure** — .env files committed, secrets in client-side code, keys in URLs
3. **Injection** — SQL injection, command injection, XSS, template injection
4. **Auth issues** — Missing auth checks, broken access control, exposed endpoints
5. **Data exposure** — Sensitive data in logs, error messages, URLs, localStorage
6. **Dependencies** — Check package.json for known vulnerable packages

## Output Format

For each finding:

- **Location:** `file:line`
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW
- **Type:** Category from list above
- **Issue:** What's wrong (one sentence)
- **Fix:** How to fix it (one sentence)

## Summary

```
Findings: X total (C critical, H high, M medium, L low)
Safe to deploy: YES / NO
```

## Rules

- Check ALL files in the path, not just a sample
- Always check for .env files, .env.local, credentials.json
- Always check if .gitignore properly excludes sensitive files
- Do not report style issues — security only
- If no findings, say "No security issues found. Safe to deploy: YES"
