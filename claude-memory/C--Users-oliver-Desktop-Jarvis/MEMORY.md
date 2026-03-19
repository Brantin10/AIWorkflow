# Jarvis Project Memory

## Completed: Phase 0 - Deepgram STT
- Replaced faster-whisper + silero-vad with Deepgram Nova-3 streaming WebSocket
- `audio/listener.py` rewritten for deepgram-sdk v6 (recv-based, not callbacks)
- `audio/normalizer.py` + `data/normalizer.json` for coding term cleanup
- Removed: faster-whisper, silero-vad-lite, torch from requirements
- API key in .env: DEEPGRAM_API_KEY

## Completed: Phase 1 - Mode System Foundation
- `brain/modes.py`: ModeManager + ModeDefinition (6 modes, fuzzy matching, brainstorm tracking)
- `brain/tools.py`: Added get_tool_names_by_category/categories() for mode filtering
- `brain/fast_dispatch.py`: 7 mode-switching regex routes (enter/exit/brainstorm/wrap-up/status/list)
- `brain/skills_loader.py`: Added get_system_prompt_knowledge_for_categories()
- `brain/ollama_agent.py` + `brain/agent.py`: Mode-filtered tools, mode instructions, Proxima routing
- `data/modes/*.md`: 6 instruction files with graceful out-of-scope denial

## Completed: Phase 2 - Brainstorm + Proxima
- `brain/proxima.py`: Async ProximaClient (chat, research, brainstorm_summary, is_available)
- Proxima API: single-message at /v1/chat/completions, model="chatgpt"/"perplexity"/"auto"
- Brainstorm saves to `data/brainstorms/brainstorm_{ts}.json` + `.md`
- Background summary extraction via Proxima on brainstorm exit
- "wrap it up" command: mid-session summary (Proxima or fallback stats)
- Dynamic exit message with session stats (exchange count + duration)

## Completed: Phase 3 - UI Themes + Polish
- `ui/brain_renderer.py`: MODE_PALETTES dict (6 color families for orb)
- `ui/overlay.py`: set_mode() updates orb palette + mode label (QLabel)
- Mode colors: general=#FFB83C, CC=#FF4444, dev=#00FF88, brainstorm=#4488FF, morning=#FFAA22, orchestrator=#AA66FF
- UI callback: ModeManager.set_on_ui_mode_change() fires on switch
- Wired in main.py: mode_manager → ui._window.set_mode()

## Key Architecture Notes
- Primary mode: Ollama free (Qwen3 14B)
- Proxima gateway at localhost:3210 (ChatGPT + Perplexity)
- Orchestrator project at: C:\Users\oliver\Desktop\Orchestrator (Electron app)
- User prefers incremental builds, one piece at a time
- User wants short voice responses to maintain conversation flow

## User Preferences
- Name: Oliver
- OS: Windows 11 Pro
- GPU: RTX 5070 Ti
- Runs Jarvis in free/Ollama mode primarily
- Has Proxima connected to ChatGPT
