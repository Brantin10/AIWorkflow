---
title: "Pydantic Settings Config Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, fastapi, pydantic, config]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: AIResume
---

# Pydantic Settings Config Pattern

## Problem
FastAPI apps need typed configuration with .env file support and validation. Plain dicts or os.getenv() lack type safety.

## Solution
Use `pydantic-settings` BaseSettings class. Automatically loads from environment variables and .env files with type coercion.

## Code

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "My API"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./app.db"
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
```

### .env file
```
SECRET_KEY=my-production-secret
DATABASE_URL=postgresql://user:pass@localhost/mydb
DEBUG=false
FRONTEND_URL=https://myapp.com
```

## Usage
```python
from app.core.config import settings

# Type-safe access
if settings.DEBUG:
    print(f"Running {settings.APP_NAME} in debug mode")

# CORS setup
app.add_middleware(CORSMiddleware, allow_origins=[settings.FRONTEND_URL])

# JWT
token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
```

## Key Points
- Environment variables override defaults and .env values
- Boolean coercion works: `"true"`, `"1"`, `"yes"` all become `True`
- Pydantic validates types at startup — catches misconfig early
- `model_config` replaces old `class Config:` inner class (Pydantic v2)
- Singleton pattern: instantiate once, import everywhere
