---
title: "Three-Tier Safety Layer for AI Tool Execution"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, safety, ai-agent]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: JARVIS
---

# Three-Tier Safety Layer for AI Tool Execution

## Problem
AI agents that execute system commands need safety guardrails. Some operations are always safe (read file), some need user confirmation (delete file), and some must never execute (format drive).

## Solution
Three-tier verdict system: ALLOW / CONFIRM / DENY, with per-tool checker methods and regex-based blocked command patterns.

## Code

```python
from enum import Enum
from pathlib import Path
import re

class SafetyVerdict(Enum):
    ALLOW = "allow"       # Execute immediately
    CONFIRM = "confirm"   # Ask user first
    DENY = "deny"         # Never allowed

class SafetyChecker:
    def __init__(self, config):
        self._blocked_patterns = [re.compile(p, re.IGNORECASE) for p in config.blocked_commands]
        self._allowed_dirs = [Path(d).resolve() for d in config.allowed_directories]

    def check(self, tool_name: str, params: dict) -> SafetyResult:
        # Route to per-tool checker if it exists
        checker = getattr(self, f"_check_{tool_name}", None)
        if checker:
            result = checker(params)
            if result:
                return result

        # Default: check confirmation list
        if tool_name in config.confirmation_required_tools:
            return SafetyResult(SafetyVerdict.CONFIRM, ...)

        return SafetyResult(SafetyVerdict.ALLOW, ...)

    def _check_run_command(self, params):
        command = params.get("command", "")
        # Check blocked patterns (format drives, disable firewall, etc.)
        for pattern in self._blocked_patterns:
            if pattern.search(command):
                return SafetyResult(SafetyVerdict.DENY, ...)
        # Check safe read-only commands (Get-Date, ipconfig, etc.)
        for pattern in self.SAFE_COMMAND_PATTERNS:
            if re.match(pattern, command.strip(), re.IGNORECASE):
                return SafetyResult(SafetyVerdict.ALLOW, ...)
        return SafetyResult(SafetyVerdict.CONFIRM, ...)

    def _is_path_allowed(self, path: Path) -> bool:
        resolved = path.resolve()
        return any(resolved.is_relative_to(d) for d in self._allowed_dirs)
```

## Blocked Command Examples
```python
blocked_commands = [
    r"format\s+[a-zA-Z]:",           # Format drives
    r"Remove-Item\s+-Recurse.*C:\Windows",
    r"Stop-Service\s+WinDefend",      # Disable Defender
    r"bcdedit",                        # Boot config
    r"diskpart",                       # Disk partition
    r"netsh\s+advfirewall.*off",      # Disable firewall
]
```

## Key Points
- `getattr(self, f"_check_{tool_name}")` provides clean per-tool routing
- Safe read-only commands (Get-Process, ipconfig) skip confirmation
- Path whitelist prevents file operations outside user directories
- Dry-run mode allows everything but logs without executing
