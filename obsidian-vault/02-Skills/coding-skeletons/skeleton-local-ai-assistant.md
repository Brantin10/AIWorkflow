---
title: "Skeleton: Local AI Voice Assistant"
type: skeleton
stack: "Python"
category: "ai"
tags:
  - skill
  - skill/skeleton
  - stack/python
  - stack/ai
---
# Skeleton: Local AI Voice Assistant

## Use Case
Desktop AI assistants with voice I/O, tool calling, mode system, and system automation. Used in [[01-Projects/jarvis]].

## File Structure
```
project/
  main.py                # Boot sequence, mode selection, CLI/UI entry
  config.py              # Centralized dataclass config (all settings)
  brain/
    agent.py             # Cloud LLM client (Claude API)
    ollama_agent.py      # Local LLM client (Ollama, drop-in replacement)
    tools.py             # Tool registry + JSON schemas
    tool_executor.py     # Execute tool calls safely
    modes.py             # Scoped execution contexts
    intent_classifier.py # Tiered ML intent routing
    fast_dispatch.py     # Regex bypass for deterministic queries
    memory.py            # SQLite conversation + action log
  audio/
    listener.py          # Streaming STT (Deepgram WebSocket)
    tts.py               # Local TTS (Kokoro ONNX + effects)
    wake_word.py         # Wake word detection
  system/
    executor.py          # PowerShell runner, app launcher
    safety.py            # Command blocklist, confirmation logic
  ui/
    app.py               # Voice loop + state machine
    overlay.py           # Desktop overlay window
  skills/
    skill-name/
      skill.json         # Schema definition
      handler.py         # Implementation
  data/
    modes/               # Mode instruction prompts (.md)
    models/              # ML model files (.pkl)
  .env                   # API keys
```

## Key Patterns
- **Dual-mode AI**: Cloud (Claude) + Local (Ollama) with same interface
- **Mode system**: Isolated execution contexts (general, developer, brainstorm, etc.)
- **Tiered intent**: Regex → TF-IDF → Semantic (fast to slow fallback)
- **Fast dispatch**: Skip LLM for deterministic queries (time, weather, mode switch)
- **Skills ecosystem**: Self-contained handler.py + schema.json per skill
- **Safety layer**: Regex blocklist + confirmation + allowed dirs + dry-run

## Setup Commands
```bash
python -m venv .venv && .venv/Scripts/activate
pip install anthropic deepgram-sdk kokoro-onnx pyside6 sounddevice
# For local: ollama serve && ollama pull qwen3:14b
python main.py --cli   # Text mode
python main.py --ui    # Voice + desktop overlay
```

## Customization Points
- Add modes in `brain/modes.py` + instruction files in `data/modes/`
- Add tools in `brain/tools.py` + handlers in `system/executor.py`
- Add skills as folders in `skills/`
- Switch LLM by changing config.mode (claude vs ollama)
