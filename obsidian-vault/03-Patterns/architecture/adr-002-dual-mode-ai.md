---
title: "ADR: Dual-mode AI architecture (Cloud + Local)"
type: adr
status: accepted
project: "JARVIS"
date: "2026-03-18"
tags:
  - adr
  - pattern
  - stack/python
  - stack/ai
---
# ADR: Dual-Mode AI Architecture (Cloud + Local)

## Context
JARVIS needs an LLM for reasoning and tool calling. Cloud APIs (Claude) are powerful but cost money. Local models (Ollama) are free but less capable.

## Decision
Implement both as drop-in replacements with the same interface: `async def think(user_input) -> response`. User selects mode at boot.

- **Premium**: Claude Sonnet 4 via Anthropic API
- **Free**: Qwen3 14B via Ollama (runs on RTX 5070 Ti GPU)

Both use the same tool registry but different schema formats:
- Claude: `to_claude_schema()`
- Ollama: `to_openai_schema()` (OpenAI-compatible format)

## Consequences
- Zero cost option for daily use (Ollama runs locally)
- Premium option for complex reasoning tasks
- Same skills/tools work in both modes
- Trade-off: Local model is less accurate for tool calling
- Ollama needs `keep_alive: 60m` to avoid VRAM thrashing (default 5m)

## Alternatives Considered
- Cloud only: Too expensive for daily personal assistant
- Local only: Tool calling accuracy too low for reliable automation
