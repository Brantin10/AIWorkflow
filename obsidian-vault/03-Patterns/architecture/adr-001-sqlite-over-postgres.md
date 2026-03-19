---
title: "ADR: SQLite over PostgreSQL for local development"
type: adr
status: accepted
project: "AIResume"
date: "2026-03-18"
tags:
  - adr
  - pattern
  - stack/python
  - stack/fastapi
---
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
