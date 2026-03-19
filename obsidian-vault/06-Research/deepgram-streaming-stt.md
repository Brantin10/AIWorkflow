---
title: "Deepgram Streaming STT Architecture"
created: "2026-03-18"
updated: "2026-03-18"
tags: [research, deepgram, stt, voice, websocket, ai]
status: active
type: research
usefulness: high
read-count: 0
source-project: JARVIS
---

# Deepgram Streaming STT Architecture

## Overview
Deepgram provides real-time speech-to-text via WebSocket streaming. JARVIS uses Deepgram Nova-3 with Flux turn detection for voice agent interactions.

## Key Configuration
```python
model = "nova-3"               # Best accuracy model
language = "en-US"
sample_rate = 16000
encoding = "linear16"
channels = 1
endpointing = 300              # ms silence before EndOfTurn
interim_results = True          # Partial transcripts while speaking
smart_format = False            # Disabled: breaks voice commands
punctuate = True
vad_events = True               # StartOfTurn / EndOfTurn events
```

## Dual-Model Strategy
1. **Flux model** — Real-time turn detection (when user starts/stops speaking)
2. **Nova-3 fallback** — Re-process low-confidence transcripts for correction

```python
use_nova3_correction = True     # Enable fallback on low confidence
```

## Key Findings
- `endpointing=300` gives snappy response (0.3s silence = done speaking)
- `smart_format=False` is critical — auto-formatting ("five" -> "5") breaks command parsing
- `vad_events=True` provides StartOfTurn/EndOfTurn WebSocket events for UI feedback
- `interim_results=True` shows live transcription in the UI while user speaks
- Nova-3 correction pass costs extra API credits but significantly improves accuracy on mumbled speech

## WebSocket Flow
```
1. Open WebSocket connection to Deepgram
2. Stream raw audio bytes (16kHz, 16-bit PCM)
3. Receive interim transcripts (partial, may change)
4. Receive final transcript on EndOfTurn event
5. Process final transcript through intent classifier
6. Execute action or generate response
```

## Gotchas
- WebSocket connection must be kept alive — reconnect logic needed
- Audio must be streamed in real-time chunks (not buffered)
- Sample rate mismatch causes garbled transcription
