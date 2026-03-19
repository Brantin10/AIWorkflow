---
title: "Skeleton: FastAPI + React + SQLite"
type: skeleton
stack: "Python + React"
category: "fullstack"
tags:
  - skill
  - skill/skeleton
  - stack/python
  - stack/react
---
# Skeleton: FastAPI + React + SQLite

## Use Case
Full-stack web apps with Python backend and React frontend. JWT auth, CRUD APIs, PDF generation. Used in [[01-Projects/airesume]].

## File Structure
```
project/
  backend/
    app/
      core/
        config.py          # Pydantic Settings (DATABASE_URL, SECRET_KEY)
        database.py        # SQLAlchemy engine + SessionLocal + Base
        security.py        # bcrypt hashing + JWT creation/decoding
      api/
        routes/            # FastAPI routers (auth, resources, health)
        deps.py            # Dependency injection (get_db, get_current_user)
      models/              # SQLAlchemy ORM models
      schemas/             # Pydantic request/response schemas
      services/            # Business logic (auth, PDF, etc.)
      middleware/           # Error handlers, logging
      main.py              # FastAPI app setup, CORS, routers
    requirements.txt
    .env
  frontend/
    src/
      pages/               # Route pages
      components/          # Reusable UI components
      context/             # React Context (Auth, App state)
      hooks/               # Custom hooks
      api/                 # Axios/fetch API client
      App.jsx
      main.jsx
    package.json
    .env                   # VITE_API_BASE_URL
```

## Key Files
- `config.py` — Pydantic BaseSettings loads from .env
- `database.py` — SQLite: add `check_same_thread=False` + WAL pragma
- `security.py` — bcrypt + python-jose JWT (HS256)
- `deps.py` — `get_current_user()` decodes Bearer token
- `api/client.js` — Axios with interceptors for auth header

## Setup Commands
```bash
# Backend
cd backend && python -m venv venv && venv/Scripts/activate
pip install fastapi uvicorn sqlalchemy pydantic python-jose bcrypt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

## Customization Points
- Change `DATABASE_URL` to PostgreSQL for production
- Add models in `models/` + schemas in `schemas/` + routes in `api/routes/`
- Frontend API base URL in `.env` as `VITE_API_BASE_URL`
