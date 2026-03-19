---
title: "Ollama Local LLM Performance Tuning"
created: "2026-03-18"
updated: "2026-03-18"
tags: [research, ollama, llm, performance, gpu, ai]
status: active
type: research
usefulness: high
read-count: 0
source-project: JARVIS
---

# Ollama Local LLM Performance Tuning

## Overview
Ollama runs LLMs locally on GPU. JARVIS uses it for free-mode operation with Qwen3 14B on RTX 5070 Ti + 64GB RAM.

## Recommended Configuration
```python
@dataclass
class OllamaConfig:
    base_url: str = "http://localhost:11434"
    model: str = "qwen3:14b"
    temperature: float = 0.1       # Low temp for reliable tool calling
    max_tokens: int = 1024
    num_ctx: int = 8192            # Context window (tokens)
    keep_alive: str = "60m"        # Keep model in VRAM
    num_gpu: int = -1              # Auto-detect (all layers to GPU)
    num_batch: int = 512           # Prompt eval batch size
```

## Key Performance Parameters

### keep_alive
- Default: `"5m"` (unloads from VRAM after 5 min idle)
- Recommended: `"60m"` for active assistant use
- Cold start after unload: ~10 seconds
- Hot inference: ~100-500ms first token

### num_ctx (Context Window)
- `4096`: Fast, but clips long conversations
- `8192`: Good balance (JARVIS default)
- `16384`: Slower, uses more VRAM
- Rule: each 4K context adds ~1GB VRAM

### num_batch (Batch Size)
- Higher = faster prompt evaluation
- `512` works well on RTX 5070 Ti (16GB VRAM)
- Reduce if hitting OOM errors

### num_gpu
- `-1`: Auto-detect, offload all layers
- Positive integer: limit GPU layers (for low VRAM)

## Model Recommendations (2026)
| Model | VRAM | Tool Calling | Speed | Quality |
|-------|------|-------------|-------|---------|
| Qwen3 14B | ~10GB | Excellent | Good | High |
| Llama 3.1 8B | ~6GB | Fair | Fast | Medium |
| Mistral 7B | ~5GB | Poor | Fastest | Medium |
| Qwen3 8B | ~6GB | Good | Fast | Medium |

## Gotchas
- First request after model load is slow (model initialization)
- Long system prompts count against context window
- Tool schemas consume ~500-1000 tokens — send only relevant tools
- Temperature > 0.3 makes tool calling unreliable
