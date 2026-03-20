#!/usr/bin/env python3
"""
Claude Code Stop Hook — Saves session to Obsidian vault + Orchestrator.

Triggered every time Claude finishes a response.
1. ALWAYS: Appends to daily vault log (claude-session-{date}.md)
   - Includes CWD (which project), stop reason, session ID
   - Cross-references today's change log for context
2. IF ORCHESTRATOR RUNNING: Also logs activity to .ai-hub/log.md
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

VAULT_PATH = Path(r"C:\Users\oliver\Obsidian\DevVault")
CLAUDE_LOG_DIR = VAULT_PATH / "01-Projects" / "claude-code-logs"
CLAUDE_LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_project_name(cwd: str) -> str:
    """Extract project name from CWD."""
    cwd_clean = cwd.replace("\\", "/").rstrip("/")
    # If in a Desktop project folder, return the project name
    desktop = "C:/Users/oliver/Desktop/"
    if cwd_clean.lower().startswith(desktop.lower()):
        remainder = cwd_clean[len(desktop):]
        return remainder.split("/")[0] if remainder else "Desktop"
    return Path(cwd_clean).name


def get_recent_changes() -> str:
    """Read today's change log to see what files were touched recently."""
    today = datetime.now().strftime("%Y-%m-%d")
    changes_path = CLAUDE_LOG_DIR / f"claude-changes-{today}.md"
    if not changes_path.exists():
        return ""

    try:
        lines = changes_path.read_text(encoding="utf-8").strip().split("\n")
        # Get last 5 file changes (skip header lines)
        file_lines = [l for l in lines if l.startswith("- `")]
        recent = file_lines[-5:] if len(file_lines) > 5 else file_lines
        if recent:
            return "Recent files: " + ", ".join(
                l.split("`")[-2] if "`" in l else l
                for l in recent
            )
    except Exception:
        pass
    return ""


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    log_path = CLAUDE_LOG_DIR / f"claude-session-{today}.md"

    # Read event data from stdin (Claude sends JSON)
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        event = {}

    # Extract what we can from the stop event
    stop_reason = event.get("stop_reason", "unknown")
    session_id = event.get("session_id", "")[:8] if event.get("session_id") else ""
    cwd = os.getcwd()
    project = get_project_name(cwd)

    # --- 1. ALWAYS: Write to Obsidian vault ---
    if not log_path.exists():
        header = f"""---
title: Claude Code Session — {today}
type: claude-log
date: {today}
tags: [claude-code, session-log]
---

# Claude Code Sessions — {today}

"""
        log_path.write_text(header, encoding="utf-8")

    # Build richer entry
    entry = f"\n## {now} — {project}\n"
    entry += f"- Stop reason: `{stop_reason}`\n"
    if session_id:
        entry += f"- Session: `{session_id}`\n"

    # Add recent file changes for context
    recent = get_recent_changes()
    if recent:
        entry += f"- {recent}\n"

    entry += "\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)

    # --- 2. BEST-EFFORT: Log to Orchestrator if running ---
    try:
        import orchestrator_client as orch

        if orch.is_running():
            project_name = orch.detect_project(cwd)
            if project_name:
                orch.log_activity(
                    project_name,
                    agent="claude-code",
                    action="Task completed",
                    detail=f"stop={stop_reason}",
                )
    except Exception:
        pass  # Never let Orchestrator errors break vault logging


if __name__ == "__main__":
    main()
