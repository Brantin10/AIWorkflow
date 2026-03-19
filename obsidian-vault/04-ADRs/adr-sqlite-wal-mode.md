---
title: "ADR: SQLite WAL Mode for Concurrent Access"
created: "2026-03-18"
updated: "2026-03-18"
tags: [adr, architecture, sqlite, database, performance]
status: active
type: adr
usefulness: high
read-count: 0
source-project: JARVIS
---

# ADR: SQLite WAL Mode for Concurrent Access

## Status
Accepted

## Context
Both JARVIS and AIResume use SQLite. JARVIS has a background flush thread writing while the main thread reads. AIResume serves concurrent FastAPI requests. Default SQLite journal mode (`DELETE`) locks the entire database during writes.

## Decision
Enable WAL (Write-Ahead Logging) mode on all SQLite databases.

### JARVIS (Python)
```python
self.conn.execute("PRAGMA journal_mode=WAL")
self.conn.execute("PRAGMA cache_size=-64000")       # 64MB page cache
self.conn.execute("PRAGMA mmap_size=268435456")      # 256MB memory-mapped I/O
self.conn.execute("PRAGMA temp_store=MEMORY")        # Temp tables in RAM
self.conn.execute("PRAGMA synchronous=NORMAL")       # Faster writes (WAL protects)
```

### AIResume (SQLAlchemy)
```python
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_conn, _):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()
```

## Consequences
### Positive
- Concurrent readers while writer commits (no read blocking)
- Faster writes (appends to WAL file, no full page copy)
- Crash-safe (WAL + checkpointing)
- `synchronous=NORMAL` safe with WAL (vs FULL needed without WAL)

### Negative
- Creates `-wal` and `-shm` files alongside the database
- WAL file can grow large under heavy write load (auto-checkpoints at 1000 pages)
- Not suitable for network-mounted filesystems (NFS)

### Performance PRAGMAs Explained
- `cache_size=-64000`: 64MB page cache (default ~2MB) — leverages available RAM
- `mmap_size=256MB`: Memory-mapped I/O for reads — bypasses read() syscalls
- `temp_store=MEMORY`: Temp tables in RAM instead of disk
- `synchronous=NORMAL`: Skips fsync on every commit (WAL handles durability)
