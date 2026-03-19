---
title: "Ollama Tool Calling Issues"
created: "2026-03-18"
updated: "2026-03-18"
tags: [playbook, ollama, llm, tool-calling, debugging]
status: active
type: playbook
usefulness: high
read-count: 0
source-project: JARVIS
---

# Ollama Tool Calling Issues

## Symptom
Ollama model calls wrong tools, sends malformed JSON arguments, or ignores tools entirely.

## Common Issues & Fixes

### 1. Too Many Tools
**Problem:** Sending 20+ tool schemas overwhelms the model's context.
**Fix:** Category-based tool selection — only send relevant tools per query:
```python
# Instead of all tools:
tools = registry.get_openai_tools()
# Send only relevant categories:
tools = registry.get_openai_tools(categories=["files", "system"])
```

### 2. Model Ignores Tools
**Problem:** Model responds with text instead of calling a tool.
**Fix:** Use lower temperature (0.1) and explicitly prompt tool usage in system message:
```
You have tools available. When the user asks to DO something, use the appropriate tool.
Do NOT describe what you would do — actually call the tool.
```

### 3. Malformed JSON in Tool Arguments
**Problem:** Model generates invalid JSON (trailing commas, unquoted keys).
**Fix:** Parse with fallback:
```python
import json, re
try:
    args = json.loads(raw_args)
except json.JSONDecodeError:
    # Try fixing common issues
    fixed = re.sub(r',\s*}', '}', raw_args)  # trailing commas
    fixed = re.sub(r',\s*]', ']', fixed)
    args = json.loads(fixed)
```

### 4. Model Choice Matters
**Tested models (2026):**
- **Qwen3 14B** — Best tool calling reliability + reasoning. Recommended.
- **Llama 3.1 8B** — Decent but sometimes skips tools
- **Mistral 7B** — Fast but unreliable tool calling

### 5. keep_alive Setting
**Problem:** Model unloads from VRAM after 5 minutes (default), causing 10s cold start.
**Fix:** Set `keep_alive: "60m"` in Ollama config to keep model loaded.

### 6. Context Window
**Problem:** Long conversations + many tools exceed context window.
**Fix:** Set `num_ctx: 8192` and trim conversation history to last 20 turns.
