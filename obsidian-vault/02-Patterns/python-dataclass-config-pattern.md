---
title: "Python Dataclass Config Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, config, dataclass]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: JARVIS
---

# Python Dataclass Config Pattern

## Problem
Application needs centralized, typed configuration with environment variable overrides, sub-configs for different modules, and validation.

## Solution
Nested `@dataclass` classes with `field(default_factory=...)` for env var loading. Master config composes sub-configs. `load_config()` factory function.

## Code

```python
import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)
PROJECT_ROOT = Path(__file__).parent.resolve()

@dataclass
class LLMConfig:
    api_key: str = field(default_factory=lambda: os.getenv("API_KEY", ""))
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 512
    temperature: float = 0.3

@dataclass
class AudioConfig:
    voice_enabled: bool = True
    tts_voice: str = "bm_george"
    tts_speed: float = 1.3
    sample_rate: int = 16000

@dataclass
class SafetyConfig:
    dry_run: bool = False
    confirmation_required_tools: list = field(default_factory=lambda: [
        "run_command", "delete_file", "click_at"
    ])
    blocked_commands: list = field(default_factory=lambda: [
        r"format\s+[a-zA-Z]:", r"bcdedit", r"diskpart"
    ])

@dataclass
class AppConfig:
    """Master config — composes all sub-configs."""
    llm: LLMConfig = field(default_factory=LLMConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    mode: str = "premium"  # "free" or "premium"

    def validate(self) -> list[str]:
        warnings = []
        if self.mode == "premium" and not self.llm.api_key:
            warnings.append("API key not set.")
        return warnings

def load_config() -> AppConfig:
    return AppConfig()
```

## Key Points
- `field(default_factory=lambda: os.getenv(...))` loads env vars at instantiation time
- Nested dataclasses give each module its own typed config namespace
- `validate()` method returns warnings instead of raising (app can still boot)
- `load_dotenv(override=True)` ensures .env values take precedence
- Lists in defaults must use `field(default_factory=lambda: [...])` — not bare `[]`
