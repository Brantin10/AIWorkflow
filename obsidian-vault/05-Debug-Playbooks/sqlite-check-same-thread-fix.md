---
title: "SQLite check_same_thread Error Fix"
created: "2026-03-18"
updated: "2026-03-18"
tags: [playbook, sqlite, python, threading, debugging]
status: active
type: playbook
usefulness: high
read-count: 0
source-project: JARVIS
---

# SQLite check_same_thread Error Fix

## Symptom
```
ProgrammingError: SQLite objects created in a thread can only be used in that same thread.
```

## Root Cause
SQLite's default Python binding enforces single-thread access. If you create a connection in thread A and use it in thread B, this error fires.

## Fix

### Python (raw sqlite3)
```python
conn = sqlite3.connect(db_path, check_same_thread=False)
```

### SQLAlchemy
```python
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
```

## Important Safety Notes
- `check_same_thread=False` disables the safety check — you must handle thread safety yourself
- Use a `threading.Lock` around all write operations
- Enable WAL mode for concurrent read/write safety: `PRAGMA journal_mode=WAL`
- FastAPI with SQLAlchemy: use `SessionLocal()` per request (dependency injection via `get_db()`)
- JARVIS pattern: single connection + write lock + background flush thread

## When NOT to Disable
- If you can restructure to use one connection per thread, prefer that
- SQLAlchemy's connection pool handles this automatically for most web frameworks
