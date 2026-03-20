"""
Shared helper for communicating with the Orchestrator REST API (port 3211).

All calls are best-effort — if Orchestrator isn't running, everything
returns None/empty gracefully. Zero impact on Claude Code when Orchestrator is off.
"""

import json
import os
import urllib.request
import urllib.error
from pathlib import Path

ORCHESTRATOR_URL = "http://localhost:3211"
TIMEOUT = 3  # seconds — fail fast if Orchestrator isn't running


def _get(path: str) -> dict | list | None:
    """GET from Orchestrator API. Returns parsed JSON or None on failure."""
    try:
        req = urllib.request.Request(f"{ORCHESTRATOR_URL}{path}")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError):
        return None


def _post(path: str, data: dict) -> dict | None:
    """POST JSON to Orchestrator API. Returns parsed JSON or None on failure."""
    try:
        body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            f"{ORCHESTRATOR_URL}{path}",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError):
        return None


def is_running() -> bool:
    """Check if Orchestrator is online."""
    result = _get("/api/health")
    return result is not None


def detect_project(cwd: str) -> str | None:
    """Match CWD against Orchestrator's registered projects.

    Returns project name if found, None otherwise.
    """
    projects = _get("/api/projects")
    if not projects:
        return None

    cwd_lower = cwd.replace("\\", "/").rstrip("/").lower()

    for proj in projects:
        proj_path = (proj.get("path") or "").replace("\\", "/").rstrip("/").lower()
        if proj_path and cwd_lower.startswith(proj_path):
            return proj.get("name")

    return None


def get_project_context(project_name: str) -> dict | None:
    """Get project context (CLAUDE.md + .ai-hub files)."""
    return _get(f"/api/projects/{project_name}/context")


def get_project_tasks(project_name: str) -> dict | None:
    """Get project tasks and activity log."""
    return _get(f"/api/projects/{project_name}/tasks")


def get_project_phases(project_name: str) -> list | None:
    """Get project phases."""
    return _get(f"/api/projects/{project_name}/phases")


def log_activity(project_name: str, agent: str, action: str, detail: str = "") -> bool:
    """Append to project activity log via .ai-hub/log.md."""
    # Write directly to the .ai-hub/log.md file since Orchestrator
    # may not have a dedicated POST endpoint for log appending.
    projects = _get("/api/projects")
    if not projects:
        return False

    for proj in projects:
        if proj.get("name") == project_name:
            proj_path = proj.get("path", "")
            log_path = Path(proj_path) / ".ai-hub" / "log.md"
            if log_path.exists():
                try:
                    from datetime import datetime
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")
                    entry = f"- [{now}] **{agent}**: {action}"
                    if detail:
                        entry += f" — {detail}"
                    entry += "\n"
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(entry)
                    return True
                except OSError:
                    return False
    return False


def get_vault_context_bundle(project_name: str) -> str | None:
    """Get vault context bundle for a project (patterns, ADRs, etc)."""
    result = _get(f"/api/vault/context-bundle?project={project_name}")
    if result and isinstance(result, dict):
        return result.get("content") or result.get("bundle") or str(result)
    return None
