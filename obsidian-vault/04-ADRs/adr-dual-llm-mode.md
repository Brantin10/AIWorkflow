---
title: "ADR: Dual LLM Mode (Free Ollama vs Premium Claude)"
created: "2026-03-18"
updated: "2026-03-18"
tags: [adr, architecture, llm, ollama, anthropic]
status: active
type: adr
usefulness: high
read-count: 0
source-project: JARVIS
---

# ADR: Dual LLM Mode (Free Ollama vs Premium Claude)

## Status
Accepted

## Context
JARVIS needs an LLM backend for conversational AI and tool calling. Claude API provides high quality but costs money per request. Local LLMs via Ollama are free but lower quality.

## Decision
Support both modes controlled by a single config flag (`mode: "free" | "premium"`):
- **Free mode:** Ollama running locally (Qwen3 14B) — zero API costs, runs on RTX 5070 Ti
- **Premium mode:** Claude Sonnet 4 via Anthropic API — higher quality, costs per token

Both agents implement the same interface: `think(user_input) -> response`. The tool registry serves schemas in both OpenAI (Ollama) and Claude formats from the same definitions.

## Consequences
### Positive
- Users can run JARVIS indefinitely for free with local models
- Premium mode available when quality matters (complex tasks)
- Single tool registry serves both formats — no duplication
- Can switch modes at runtime via config

### Negative
- Must maintain two agent implementations (OllamaAgent, JarvisAgent)
- Tool calling reliability differs between models (Qwen3 vs Claude)
- Ollama requires GPU + model download (~8GB for Qwen3 14B)

## Alternatives Considered
- **Claude-only:** Simpler but creates API cost dependency
- **Ollama-only:** Free but tool calling less reliable
- **OpenRouter proxy:** Single API, multiple models — adds network dependency
