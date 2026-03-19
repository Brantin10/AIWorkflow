---
title: "Python Voice Assistant Skeleton"
created: "2026-03-18"
updated: "2026-03-18"
tags: [skeleton, python, voice, ai-agent, deepgram, tts]
status: active
type: skeleton
usefulness: high
read-count: 0
source-project: JARVIS
---

# Python Voice Assistant Skeleton

Desktop voice assistant with STT, LLM agent, tool execution, TTS, and safety layer.

## Structure
```
assistant/
  main.py               # Boot + main loop
  config.py             # Dataclass-based config
  brain/
    __init__.py
    agent.py            # LLM agent (Claude/Ollama)
    tools.py            # Tool registry (JSON Schema definitions)
    memory.py           # SQLite + semantic embeddings
    intent_classifier.py # Chat vs command routing
    fast_dispatch.py    # Regex-based instant routing (skip LLM)
    router.py           # Model selection by complexity
  system/
    __init__.py
    executor.py         # Tool execution engine
    safety.py           # ALLOW/CONFIRM/DENY safety layer
  audio/
    __init__.py
    stt.py              # Speech-to-text (Deepgram WebSocket)
    tts.py              # Text-to-speech (Kokoro ONNX)
    wake_word.py        # Wake word detection
  ui/
    __init__.py
    orb.py              # Floating desktop orb (pywebview)
  data/
    jarvis.db           # SQLite database
    models/             # Trained ML models (pickled)
  skills/               # Markdown skill definitions
  requirements.txt
  .env
```

## Boot Sequence
```python
async def main():
    config = load_config()

    # 1. Initialize systems
    memory = MemoryManager(config.database)
    tools = ToolRegistry()
    safety = SafetyChecker(config.safety)
    executor = Executor(safety)
    agent = Agent(config, tools, memory, executor)

    # 2. Load optional subsystems
    intent = IntentClassifier()
    intent.load()  # Load pickled ML models
    memory.backfill_embeddings()  # Background thread

    # 3. Start interaction loop
    if args.cli:
        await cli_loop(agent)
    else:
        start_ui(agent)  # Floating orb + voice
```

## Key Dependencies
```
# LLM
anthropic>=0.42.0    # Claude API
openai>=1.0.0        # Ollama compatibility

# Voice
deepgram-sdk>=4.0.0  # STT (WebSocket streaming)
kokoro-onnx>=0.4.0   # TTS (local ONNX)
sounddevice>=0.5.0   # Microphone/speaker

# System
psutil>=6.0.0        # System monitoring
pyautogui>=0.9.54    # Screenshot + automation

# ML
scikit-learn>=1.4.0  # Intent classifier
model2vec>=0.7.0     # Semantic embeddings

# UI
pywebview>=5.0       # Desktop window
pystray>=0.19.0      # System tray
pynput>=1.7.0        # Global hotkeys
```
