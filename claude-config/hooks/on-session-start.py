#!/usr/bin/env python3
"""
Claude Code SessionStart Hook — Loads vault + Orchestrator context.

On every new session:
1. Reads recent patterns, projects, and session logs from Obsidian vault
2. If Orchestrator is running, pulls active project tasks, plan, and phase info
3. Prints everything to stdout so Claude starts with full context
"""

import sys
import io
import os
from datetime import datetime, timedelta
from pathlib import Path

# Fix Windows console encoding (cp1252 can't handle unicode)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Allow importing orchestrator_client from same directory
sys.path.insert(0, str(Path(__file__).parent))

VAULT_PATH = Path(r"C:\Users\oliver\Obsidian\DevVault")


def get_recent_lessons(days=3) -> str:
    """Read recent debug playbooks and pattern notes."""
    lines = []
    cutoff = datetime.now() - timedelta(days=days)

    for folder in ["05-Debug-Playbooks", "02-Patterns", "03-Patterns"]:
        pattern_dir = VAULT_PATH / folder
        if not pattern_dir.exists():
            continue
        for f in sorted(pattern_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]:
            if datetime.fromtimestamp(f.stat().st_mtime) > cutoff:
                lines.append(f"- Recent pattern: {f.stem}")

    return "\n".join(lines) if lines else ""


def get_active_projects() -> str:
    """Read active project notes."""
    lines = []
    projects_dir = VAULT_PATH / "01-Projects"
    if not projects_dir.exists():
        return ""

    for f in sorted(projects_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
        lines.append(f"- Active project: {f.stem}")

    return "\n".join(lines) if lines else ""


def get_recent_session_log() -> str:
    """Read today's or yesterday's Claude session log."""
    log_dir = VAULT_PATH / "01-Projects" / "claude-code-logs"
    if not log_dir.exists():
        return ""

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    for date in [today, yesterday]:
        log_path = log_dir / f"claude-session-{date}.md"
        if log_path.exists():
            content = log_path.read_text(encoding="utf-8")
            if len(content) > 500:
                return f"Recent session context ({date}):\n...{content[-500:]}"
            return f"Recent session context ({date}):\n{content}"

    return ""


def get_orchestrator_context() -> str:
    """Pull project context from Orchestrator if it's running."""
    try:
        import orchestrator_client as orch

        if not orch.is_running():
            return ""

        # Detect which project we're in based on CWD
        cwd = os.getcwd()
        project_name = orch.detect_project(cwd)
        if not project_name:
            return ""

        lines = [f"[Orchestrator] Active project: {project_name}"]

        # Get tasks
        tasks = orch.get_project_tasks(project_name)
        if tasks:
            task_content = tasks.get("tasks") or tasks.get("content", "")
            if isinstance(task_content, str) and task_content.strip():
                # Extract just the "In Progress" section if possible
                in_progress = ""
                for section in task_content.split("##"):
                    if "in progress" in section.lower() or "current" in section.lower():
                        in_progress = section.strip()[:300]
                        break
                if in_progress:
                    lines.append(f"Current tasks:\n{in_progress}")

        # Get phases
        phases = orch.get_project_phases(project_name)
        if phases and isinstance(phases, list):
            active = [p for p in phases if p.get("status") in ("active", "in-progress", "current")]
            if active:
                phase_names = ", ".join(p.get("name", p.get("title", "?")) for p in active[:3])
                lines.append(f"Active phases: {phase_names}")

        return "\n".join(lines)

    except Exception:
        return ""


def main():
    parts = []

    # Vault context
    lessons = get_recent_lessons()
    if lessons:
        parts.append(f"## Recent Vault Patterns\n{lessons}")

    projects = get_active_projects()
    if projects:
        parts.append(f"## Active Projects\n{projects}")

    session_log = get_recent_session_log()
    if session_log:
        parts.append(f"## Last Session\n{session_log}")

    # Orchestrator context (best-effort, skipped if not running)
    orch_context = get_orchestrator_context()
    if orch_context:
        parts.append(f"## Orchestrator\n{orch_context}")

    if parts:
        output = "Obsidian Vault Context:\n\n" + "\n\n".join(parts)
        print(output)


if __name__ == "__main__":
    main()
