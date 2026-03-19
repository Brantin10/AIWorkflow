---
title: "ADR: Fast Dispatch — Skip LLM for Deterministic Queries"
created: "2026-03-18"
updated: "2026-03-18"
tags: [adr, architecture, performance, llm, optimization]
status: active
type: adr
usefulness: high
read-count: 0
source-project: JARVIS
---

# ADR: Fast Dispatch — Skip LLM for Deterministic Queries

## Status
Accepted

## Context
Many voice commands always map to the same tool with the same parameters:
- "What time is it?" always calls `get_time()`
- "Take a screenshot" always calls `take_screenshot()`
- "Check my CPU" always calls `get_system_info(info_type="cpu")`

Routing these through the LLM adds 1-15 seconds of latency for zero value.

## Decision
Add a `FastDispatch` layer that runs BEFORE the LLM. It uses regex patterns to match deterministic queries and calls the tool directly, returning a formatted response in ~50ms.

```
User input -> FastDispatch (regex match?)
  Yes -> Execute tool directly -> Return response (50ms)
  No  -> LLM agent (1-15s)
```

Each dispatch route is a `(regex_pattern, async_handler)` pair. The handler receives the regex match and the executor, and returns either a `DispatchResult` or `None` (falls through to LLM).

## Consequences
### Positive
- 50ms response for common queries instead of 1-15s
- Reduces API costs (fewer LLM calls)
- Feels more responsive for voice interactions
- Easy to add new deterministic routes

### Negative
- Regex patterns must be carefully tuned to avoid false positives
- Formatted responses are hardcoded (less natural than LLM-generated)
- New tools need explicit fast-dispatch routes to benefit

## Key Metrics
- Fast dispatch handles ~30% of all queries
- Average response time: 50ms (vs 3-15s through LLM)
