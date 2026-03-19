---
title: "Debug: httpx 307 redirects with FastAPI"
type: debug-playbook
category: "api"
stack: "Python"
date: "2026-03-18"
tags:
  - debug
  - pattern
  - stack/python
  - stack/fastapi
---
# Debug: httpx 307 Redirects with FastAPI

## Symptoms
- POST/PUT requests return 307 Temporary Redirect instead of expected response
- Data appears to be lost (redirected GET has no body)
- Works fine in browser but fails in scripts

## Root Cause
FastAPI returns 307 redirect when URL has trailing slash mismatch:
- Route defined as `/resumes/` but client sends to `/resumes`
- httpx does NOT follow redirects by default (unlike requests library)

## Fix
```python
# Use follow_redirects=True
client = httpx.Client(follow_redirects=True)
response = client.post("http://localhost:8000/api/resumes", json=data)
```

Or ensure URL matches route exactly (with or without trailing slash).

## Prevention
- Always use `httpx.Client(follow_redirects=True)` for API scripts
- Be consistent with trailing slashes in FastAPI route definitions
- Test with `curl -L` (follows redirects) to verify
