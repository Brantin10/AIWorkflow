#!/usr/bin/env python3
"""
Claude Code PostToolUse Hook — Tracks file changes in Obsidian + Orchestrator.

Fires after every Write/Edit tool use.
1. ALWAYS: Logs to vault (claude-changes-{date}.md)
2. IF ORCHESTRATOR RUNNING: Also logs to .ai-hub/log.md
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


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    # Extract file path from the tool input
    tool_input = event.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    tool_name = event.get("tool_name", "unknown")

    if not file_path:
        return

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")
    log_path = CLAUDE_LOG_DIR / f"claude-changes-{today}.md"

    # --- 1. ALWAYS: Write to Obsidian vault ---
    if not log_path.exists():
        header = f"""---
title: Claude Code Changes — {today}
type: change-log
date: {today}
tags: [claude-code, changes]
---

# Files Modified by Claude — {today}

"""
        log_path.write_text(header, encoding="utf-8")

    # Shorten path for readability
    short_path = file_path.replace("C:\\Users\\oliver\\Desktop\\", "~/")
    short_path = short_path.replace("C:/Users/oliver/Desktop/", "~/")
    short_path = short_path.replace("C:\\Users\\oliver\\", "~user/")
    short_path = short_path.replace("C:/Users/oliver/", "~user/")

    # Detect project from file path
    fp = file_path.replace("\\", "/")
    project = ""
    desktop = "C:/Users/oliver/Desktop/"
    if fp.startswith(desktop):
        remainder = fp[len(desktop):]
        project = remainder.split("/")[0] if remainder else ""
    elif "/.claude/" in fp:
        project = "claude-config"
    project_tag = f" [{project}]" if project else ""

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"- `{now}` **{tool_name}**: `{short_path}`{project_tag}\n")

    # --- 2. BEST-EFFORT: Log to Orchestrator if running ---
    try:
        import orchestrator_client as orch

        if orch.is_running():
            cwd = os.getcwd()
            project_name = orch.detect_project(cwd)
            if project_name:
                orch.log_activity(
                    project_name,
                    agent="claude-code",
                    action=f"File {tool_name.lower()}",
                    detail=short_path,
                )
    except Exception:
        pass  # Never let Orchestrator errors break vault logging


if __name__ == "__main__":
    main()
