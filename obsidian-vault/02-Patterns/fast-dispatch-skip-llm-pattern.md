---
title: "Fast Dispatch Pattern — Skip LLM for Deterministic Queries"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, llm, performance, optimization]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: JARVIS
---

# Fast Dispatch Pattern — Skip LLM for Deterministic Queries

## Problem
Queries like "what time is it" always call the same tool. Routing through an LLM adds 1-15 seconds for zero value.

## Solution
Regex-matched dispatch table that runs BEFORE the LLM. Each route returns a formatted response or None (falls through to LLM).

## Code

```python
from dataclasses import dataclass
import re

@dataclass
class DispatchResult:
    response: str
    tool_name: str
    params: dict
    execution_time_ms: float = 0.0

class FastDispatch:
    def __init__(self, executor):
        self.executor = executor
        self.routes = [
            (re.compile(r"what('?s| is) the time|what time", re.I), self._handle_time),
            (re.compile(r"take a screenshot|screenshot|screen\s*grab", re.I), self._handle_screenshot),
            (re.compile(r"(check|show|what'?s?) (my |the )?(cpu|processor)", re.I), self._handle_cpu),
            (re.compile(r"(check|show|what'?s?) (my |the )?(ram|memory)", re.I), self._handle_memory),
            (re.compile(r"flip a coin|coin flip", re.I), self._handle_coin_flip),
        ]

    async def try_dispatch(self, text: str) -> DispatchResult | None:
        for pattern, handler in self.routes:
            match = pattern.search(text.strip())
            if match:
                return await handler(match)
        return None  # Fall through to LLM

    async def _handle_time(self, match):
        result = await self.executor.execute("get_time", {})
        return DispatchResult(
            response=f"It's {result.output}",
            tool_name="get_time", params={}
        )

    async def _handle_cpu(self, match):
        result = await self.executor.execute("get_system_info", {"info_type": "cpu"})
        return DispatchResult(
            response=result.output,
            tool_name="get_system_info", params={"info_type": "cpu"}
        )
```

## Integration in Agent
```python
async def think(self, user_input: str):
    # Try fast dispatch first
    fast = await self.fast_dispatch.try_dispatch(user_input)
    if fast:
        self.memory.save_action(fast.tool_name, fast.params, ...)
        return fast.response

    # Fall through to LLM
    return await self._llm_think(user_input)
```

## Key Points
- ~50ms response vs 1-15s through LLM
- Log fast-dispatch results to memory (same as LLM actions)
- Return `None` from handler to force LLM fallback
- Keep regex patterns specific to avoid false positives
