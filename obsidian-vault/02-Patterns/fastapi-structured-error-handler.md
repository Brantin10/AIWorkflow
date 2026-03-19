---
title: "FastAPI Structured Error Handler"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, fastapi, error-handling]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: AIResume
---

# FastAPI Structured Error Handler

## Problem
FastAPI default error responses have inconsistent shapes. Validation errors (422) look different from HTTP exceptions (4xx) and unhandled exceptions (500). Frontend needs a consistent format.

## Solution
Three exception handlers that all return the same JSON shape: `{ detail, code, errors? }`.

## Code

```python
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# Machine-readable error codes
_STATUS_CODES = {
    400: "BAD_REQUEST", 401: "UNAUTHORIZED", 403: "FORBIDDEN",
    404: "NOT_FOUND", 409: "CONFLICT", 422: "VALIDATION_ERROR",
    429: "RATE_LIMITED", 500: "INTERNAL_ERROR", 503: "SERVICE_UNAVAILABLE",
}

def _build_error(status_code, detail, code=None, errors=None):
    body = {"detail": detail, "code": code or _STATUS_CODES.get(status_code, "UNKNOWN")}
    if errors:
        body["errors"] = errors
    return JSONResponse(status_code=status_code, content=body)

# Handler 1: Validation errors (422)
async def validation_handler(request, exc: RequestValidationError):
    errors = [
        {"field": " -> ".join(str(l) for l in e["loc"] if l != "body"), "message": e["msg"]}
        for e in exc.errors()
    ]
    return _build_error(422, "Validation error", errors=errors)

# Handler 2: HTTP exceptions (4xx, 5xx)
async def http_handler(request, exc: HTTPException):
    return _build_error(exc.status_code, str(exc.detail))

# Handler 3: Unhandled exceptions (catch-all)
async def generic_handler(request, exc: Exception):
    if isinstance(exc, OperationalError):
        return _build_error(503, "Database unavailable.", "DATABASE_UNAVAILABLE")
    if isinstance(exc, SQLAlchemyError):
        return _build_error(500, "Database error.", "DATABASE_ERROR")
    detail = f"{type(exc).__name__}: {exc}" if DEBUG else "Unexpected error."
    return _build_error(500, detail)

# Registration
app.add_exception_handler(RequestValidationError, validation_handler)
app.add_exception_handler(HTTPException, http_handler)
app.add_exception_handler(Exception, generic_handler)
```

## Response Shape
```json
{
  "detail": "Validation error",
  "code": "VALIDATION_ERROR",
  "errors": [
    {"field": "email", "message": "value is not a valid email address"}
  ]
}
```

## Key Points
- `code` field enables frontend to match on error types programmatically
- DB connection errors return 503 (not 500) so clients can distinguish
- DEBUG mode leaks exception details; production hides them
- Register handlers in order: validation, HTTP, generic (most specific first)
