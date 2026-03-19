---
title: 'Bundle: AIResume'
type: context-bundle
project: AIResume
date: '2026-03-18'
tags:
  - bundle
---
# Context Bundle: AIResume

## Project Overview

# AIResume — AI-Powered Resume Builder

## Overview
Full-stack resume builder with PDF generation. FastAPI backend with JWT auth, SQLAlchemy ORM, and ReportLab PDF rendering. React 19 frontend with Vite, live preview, and template system.

## Stack & Tools
- **Backend:** FastAPI + SQLAlchemy + SQLite (WAL) + Pydantic + bcrypt + python-jose
- **Frontend:** React 19 + Vite 7 + React Router + Axios
- **PDF:** ReportLab + Jinja2 templates
- **Auth:** JWT (HS256) with HTTPBearer scheme
- **Testing:** pytest + httpx (backend), ESLint (frontend)

## Architecture
```
backend/
  app/
    main.py           — FastAPI app with lifespan, CORS, error handlers
    api/
      routes/         — auth, health, resumes, templates
      deps.py         — Shared dependencies (get_db, get_current_user)
    core/
      config.py       — pydantic-settings based config
      database.py     — SQLAlchemy engine + session factory
      security.py     — JWT + bcrypt password hashing
    middleware/
      error_handler.py — Structured error responses with codes
      request_logger.py — Request timing middleware
    models/           — SQLAlchemy ORM models (User, Resume)
    schemas/          — Pydantic request/response schemas
    services/         — Business logic (auth_service)
frontend/
  src/
    api/client.js     — Axios instance with auth interceptor
    context/          — AuthContext (JWT token management)
    hooks/            — useAuth, useResume
    components/       — Reusable UI components
    pages/            — Route pages
```

## Key Design Decisions
- JSON-serialized resume sections stored in single Resume table (flexible schema)
- Structured error responses with machine-readable error codes
- Axios interceptor auto-injects Bearer token and handles 401 redirect
- AuthContext validates token on mount by calling /auth/me
- CORS with explicit frontend URL origin + Content-Disposition expose header for PDF downloads

## Related Notes
- [[02-Patterns/fastapi-jwt-auth-pattern]]
- [[02-Patterns/react-auth-context-pattern]]
- [[02-Patterns/axios-interceptor-pattern]]
- [[02-Patterns/fastapi-structured-error-handler]]
- [[03-Skeletons/fastapi-react-fullstack-skeleton]]
- [[04-ADRs/adr-json-columns-for-flexible-schema]]

## Relevant Architecture Decisions

### ADR: SQLite over PostgreSQL for local development
# ADR: SQLite over PostgreSQL for Local Development

## Context
AIResume needed a database. PostgreSQL was the default choice but wasn't installed on the dev machine and requires a running server process.

## Decision
Use SQLite with WAL mode for local development. Add `check_same_thread=False` for SQLAlchemy and WAL pragma for concurrent reads.

```python
connect_args = {"check_same_thread": False}  # SQLite only
engine = create_engine(DATABASE_URL, connect_args=connect_args)

@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_conn, _):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()
```

## Consequences
- No external database server needed
- Single file (`airesume.db`) — easy to backup/reset
- WAL mode enables concurrent reads during writes
- Trade-off: No advanced PostgreSQL features (JSONB, full-text search)
- Migration path: Change `DATABASE_URL` to PostgreSQL connection string

## Alternatives Considered
- PostgreSQL: More features but requires installation and running service
- In-memory SQLite: Too ephemeral for persistent data

