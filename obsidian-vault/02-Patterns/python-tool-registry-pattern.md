---
title: "Python Tool Registry Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, llm, tool-calling]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: JARVIS
---

# Python Tool Registry Pattern

## Problem
LLM agents need a dynamic set of tools with JSON Schema definitions that can be served in both Claude and OpenAI formats, with schema caching for performance.

## Solution
Dataclass-based `ToolDefinition` with dual-format schema methods, managed by a `ToolRegistry` with lazy schema caching.

## Code

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema
    confirmation_required: bool = False
    category: str = "general"

    def to_claude_schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters,
        }

    def to_openai_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._claude_cache: list[dict] | None = None
        self._openai_cache: dict[str, dict] | None = None

    def register(self, tool: ToolDefinition):
        self._tools[tool.name] = tool
        self._claude_cache = None  # invalidate
        self._openai_cache = None

    def get_claude_tools(self) -> list[dict]:
        if self._claude_cache is None:
            self._claude_cache = [t.to_claude_schema() for t in self._tools.values()]
        return self._claude_cache

    def get_openai_tools(self, categories: list[str] | None = None) -> list[dict]:
        if self._openai_cache is None:
            self._openai_cache = {n: t.to_openai_schema() for n, t in self._tools.items()}
        if categories is None:
            return list(self._openai_cache.values())
        return [self._openai_cache[n] for n, t in self._tools.items() if t.category in categories]
```

## Usage

```python
registry = ToolRegistry()
registry.register(ToolDefinition(
    name="search_web",
    description="Search the web for a query",
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
    category="web",
))

# For Claude API
tools = registry.get_claude_tools()

# For Ollama/OpenAI
tools = registry.get_openai_tools(categories=["web"])
```

## Key Points
- Schema caches invalidate on `register()` — tools only added at boot, so invalidation is rare
- Category-based filtering lets you send only relevant tools to the LLM (reduces token usage)
- `get_openai_tools_by_names()` avoids rebuilding schemas per query
