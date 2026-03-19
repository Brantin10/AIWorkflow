---
title: "Kokoro ONNX Local Text-to-Speech"
created: "2026-03-18"
updated: "2026-03-18"
tags: [research, tts, voice, onnx, ai, local]
status: active
type: research
usefulness: high
read-count: 0
source-project: JARVIS
---

# Kokoro ONNX Local Text-to-Speech

## Overview
Kokoro is a local TTS engine that runs as an ONNX model. No API calls, no costs, no internet required. JARVIS uses it for all speech output.

## Configuration
```python
tts_voice = "bm_george"    # British male (JARVIS-like)
tts_speed = 1.3             # Brisk conversational pace
tts_volume = 0.85
sample_rate = 24000          # Kokoro native rate
```

## Available Voices
- `bm_george` — British male, authoritative (recommended for assistants)
- `bm_daniel` — British male, deeper
- `af_nicole` — American female
- `af_sarah` — American female, warm
- `bf_emma` — British female

## Audio Effects (Optional)
Using `pedalboard` library for post-processing:
```python
from pedalboard import Pedalboard, PitchShift, Reverb, Chorus

effects = Pedalboard([
    PitchShift(semitones=-1),    # Slightly deeper
    Reverb(room_size=0.1),       # Subtle room ambiance
])
processed_audio = effects(audio_array, sample_rate=24000)
```

## Key Findings
- First synthesis call is slow (~500ms) due to model loading
- Subsequent calls: ~100-200ms for short sentences
- Quality is comparable to cloud TTS (Google, Azure) for English
- Works entirely offline after model download
- Model size: ~70MB ONNX file
- No GPU required (runs on CPU)

## Audio Ducking
JARVIS lowers system volume when speaking to avoid competition:
```python
audio_ducking_enabled = True
duck_volume_percent = 20  # Lower to 20% during speech
```

## Integration
```python
import kokoro_onnx
import sounddevice as sd

model = kokoro_onnx.Kokoro("kokoro-v0_19.onnx", "voices.bin")
audio, sr = model.create("Hello, how can I help?", voice="bm_george", speed=1.3)
sd.play(audio, samplerate=sr)
sd.wait()
```
