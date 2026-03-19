---
title: "FastAPI CORS Preflight Fix"
created: "2026-03-18"
updated: "2026-03-18"
tags: [playbook, fastapi, cors, react, debugging]
status: active
type: playbook
usefulness: high
read-count: 0
source-project: AIResume
---

# FastAPI CORS Preflight Fix

## Symptom
React frontend gets CORS errors on POST/PUT/DELETE requests. GET requests work fine. Browser console shows "Access-Control-Allow-Origin" missing on preflight.

## Root Cause
Browser sends OPTIONS preflight for non-simple requests (POST with JSON, custom headers). CORSMiddleware must be configured to handle these.

## Fix

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # e.g., "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],      # Must include OPTIONS implicitly
    allow_headers=["*"],      # Must allow Authorization header
    expose_headers=["Content-Disposition"],  # For file download filenames
    max_age=600,              # Cache preflight for 10 min
)
```

## Common Mistakes
1. **Using `allow_origins=["*"]` with `allow_credentials=True`** — Browsers reject this combination. Use explicit origin.
2. **Missing `expose_headers`** — Frontend cannot read custom response headers (e.g., Content-Disposition for PDF downloads) unless explicitly exposed.
3. **Middleware order matters** — CORSMiddleware must be added AFTER other middleware that might short-circuit (request loggers are fine before it).
4. **Trailing slash mismatch** — `http://localhost:5173` != `http://localhost:5173/`. Use without trailing slash.

## Verification
```bash
# Test preflight manually
curl -X OPTIONS http://localhost:8000/api/resumes \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: authorization,content-type" -v
# Should return 200 with Access-Control-Allow-* headers
```
