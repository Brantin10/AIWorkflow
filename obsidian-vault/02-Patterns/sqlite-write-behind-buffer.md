---
title: "SQLite Write-Behind Buffer"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, sqlite, performance, threading]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: JARVIS
---

# SQLite Write-Behind Buffer

## Problem
Frequent small writes to SQLite (logging messages, actions) cause I/O overhead if each write triggers a commit. Need non-blocking writes without losing data.

## Solution
Background flush thread that commits every N seconds when dirty flag is set. All writes acquire a lock, set the dirty flag, and return immediately.

## Code

```python
import threading

class MemoryManager:
    def __init__(self):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        # Performance pragmas
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA cache_size=-64000")       # 64MB
        self.conn.execute("PRAGMA mmap_size=268435456")      # 256MB
        self.conn.execute("PRAGMA temp_store=MEMORY")
        self.conn.execute("PRAGMA synchronous=NORMAL")

        # Write-behind buffer
        self._write_dirty = threading.Event()
        self._write_stop = threading.Event()
        self._write_lock = threading.Lock()
        self._flush_thread = threading.Thread(
            target=self._flush_loop, daemon=True
        )
        self._flush_thread.start()

    def _flush_loop(self):
        while not self._write_stop.is_set():
            self._write_dirty.wait(timeout=5.0)
            if self._write_dirty.is_set():
                self._write_dirty.clear()
                with self._write_lock:
                    self.conn.commit()

    def save_message(self, role, content):
        with self._write_lock:
            self.conn.execute("INSERT INTO ...", (role, content))
        self._write_dirty.set()  # Signal flush thread

    def flush(self):
        """Force immediate commit."""
        with self._write_lock:
            self.conn.commit()
            self._write_dirty.clear()
```

## Key Points
- `check_same_thread=False` required for cross-thread SQLite access
- WAL mode enables concurrent readers while writer thread commits
- 5-second flush interval balances durability vs performance
- `flush()` method available for graceful shutdown
- daemon thread auto-dies when main process exits
