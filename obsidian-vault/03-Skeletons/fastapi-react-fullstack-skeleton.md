---
title: "FastAPI + React Fullstack Skeleton"
created: "2026-03-18"
updated: "2026-03-18"
tags: [skeleton, fastapi, react, python, javascript, fullstack]
status: active
type: skeleton
usefulness: high
read-count: 0
source-project: AIResume
---

# FastAPI + React Fullstack Skeleton

Full-stack app with FastAPI backend (JWT auth, SQLAlchemy, SQLite) and React frontend (Vite, Axios).

## Backend Structure
```
backend/
  app/
    __init__.py
    main.py
    api/
      __init__.py
      deps.py           # get_db, get_current_user
      routes/
        __init__.py
        auth.py          # POST /register, /login, GET /me
        health.py        # GET /health
    core/
      __init__.py
      config.py          # pydantic-settings
      database.py        # SQLAlchemy engine + SessionLocal
      security.py        # JWT + bcrypt
    middleware/
      __init__.py
      error_handler.py   # Structured error responses
      request_logger.py  # Request timing
    models/
      __init__.py
      user.py            # SQLAlchemy User model
    schemas/
      __init__.py
      auth.py            # LoginRequest, TokenResponse
      user.py            # UserCreate, UserResponse
    services/
      __init__.py
      auth_service.py    # register_user, authenticate_user
  requirements.txt
  .env
```

## backend/app/main.py
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.add_middleware(CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    expose_headers=["Content-Disposition"], max_age=600)
```

## backend/app/core/database.py
```python
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Enable WAL for SQLite
@event.listens_for(engine, "connect")
def _set_wal(dbapi_conn, _):
    dbapi_conn.cursor().execute("PRAGMA journal_mode=WAL")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
```

## Frontend Structure
```
frontend/
  src/
    App.jsx
    main.jsx
    api/
      client.js          # Axios with auth interceptor
      authApi.js
    context/
      AuthContext.jsx     # Auth state + token validation
    hooks/
      useAuth.js
    components/
    pages/
    routes/
      AppRouter.jsx
    styles/
  package.json
  vite.config.js
  index.html
```

## Key Dependencies
```
# Backend
fastapi, uvicorn[standard], sqlalchemy, aiosqlite
pydantic, pydantic-settings, python-jose[cryptography]
bcrypt, python-multipart, alembic

# Frontend
react, react-dom, react-router-dom, axios, vite
```

## Run
```bash
# Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm run dev  # Vite on port 5173
```
