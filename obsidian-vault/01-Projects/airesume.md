---
title: "AIResume"
created: "2026-03-18"
updated: "2026-03-18"
tags: [project, project/active, stack/fastapi, stack/react, stack/sqlite, stack/vite]
status: active
type: project
usefulness: high
read-count: 0
---

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
