---
title: "JARVIS"
created: "2026-03-18"
updated: "2026-03-18"
tags: [project, project/active, stack/python, stack/electron, stack/anthropic, stack/ollama, stack/deepgram, stack/sqlite]
status: active
type: project
usefulness: high
read-count: 0
---

# JARVIS — Local Windows 11 Voice Assistant

## Overview
AI-powered desktop voice assistant for Windows 11. Supports two runtime modes: **Premium** (Claude API) and **Free** (Ollama local LLM). Features voice I/O (Deepgram STT + Kokoro TTS), tool calling, semantic memory, and a floating desktop orb UI.

## Stack & Tools
- **Language:** Python 3.11+
- **LLM (Premium):** Anthropic Claude (Sonnet 4)
- **LLM (Free):** Ollama (Qwen3 14B)
- **STT:** Deepgram Nova-3 (WebSocket streaming)
- **TTS:** Kokoro ONNX (local, British male voice)
- **UI:** pywebview (transparent floating orb) + Electron dashboard
- **DB:** SQLite (WAL mode) with semantic embeddings (model2vec)
- **System:** psutil, pyautogui, pynput (global hotkeys)
- **Dashboard:** Flask (morning routine on port 5050)
- **Command Center:** PySide6 (Qt6)

## Architecture
```
main.py (CLI/UI boot)
  brain/
    agent.py          — Claude API agent
    ollama_agent.py   — Ollama agent (free mode)
    tools.py          — Tool registry (JSON schema definitions)
    memory.py         — SQLite + semantic search
    intent_classifier.py — Tiered ML classifier (regex > TF-IDF > Model2Vec)
    fast_dispatch.py  — Regex-based instant tool routing (skips LLM)
    router.py         — Model selection by complexity
    skills_loader.py  — Dynamic skill loading from markdown
  system/
    executor.py       — Tool execution (safety-checked)
    safety.py         — Three-tier safety layer (ALLOW/CONFIRM/DENY)
  ui/                 — Floating orb + Electron dashboard
```

## Key Design Decisions
- Dual-mode architecture (free Ollama vs paid Claude) controlled by single config flag
- Three-tier intent classification: regex fast-path > TF-IDF > Model2Vec semantic fallback
- Fast dispatch bypasses LLM entirely for deterministic queries
- Write-behind buffer for SQLite commits (background thread, flush every 5s)
- Safety layer with blocked command regex patterns and allowed directory whitelist
- Semantic memory search using model2vec embeddings stored as BLOBs

## Key Learnings
- Deepgram Flux model provides real-time turn detection (StartOfTurn/EndOfTurn events)
- Kokoro ONNX TTS runs fully local with no API costs
- SQLite WAL mode + PRAGMA tuning (64MB cache, 256MB mmap) handles concurrent read/write well
- model2vec potion-base-8M provides fast 256-dim embeddings for semantic search

## Related Notes
- [[02-Patterns/python-tool-registry-pattern]]
- [[02-Patterns/tiered-intent-classification]]
- [[02-Patterns/sqlite-write-behind-buffer]]
- [[02-Patterns/three-tier-safety-layer]]
- [[04-ADRs/adr-dual-llm-mode]]
- [[04-ADRs/adr-fast-dispatch-skip-llm]]
