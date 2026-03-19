---
title: "Debug: Pydantic email validation rejects valid TLDs"
type: debug-playbook
category: "validation"
stack: "Python"
date: "2026-03-18"
tags:
  - debug
  - pattern
  - stack/python
---
# Debug: Pydantic Email Validation Rejects Valid TLDs

## Symptoms
- Registration API returns 422 for emails like `user@app.local`
- Error: "value is not a valid email address"
- Same email works in other systems

## Root Cause
Pydantic's `email-validator` library rejects `.local` as a reserved/special-use TLD (RFC 6761). Also rejects `.test`, `.invalid`, `.example`.

## Fix
Use a real TLD for dev/testing:
- `user@app.dev` (valid, Google-owned)
- `user@test.com` (valid domain)

Or use a custom validator that's less strict about TLDs.

## Prevention
- Don't use reserved TLDs for test accounts
- Use `.dev` or `.com` domains for development testing
