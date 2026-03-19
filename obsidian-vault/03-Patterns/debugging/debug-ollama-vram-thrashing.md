---
title: "Debug: Ollama VRAM thrashing (model unload/reload)"
type: debug-playbook
category: "ai"
stack: "Python"
date: "2026-03-18"
tags:
  - debug
  - pattern
  - stack/python
  - stack/ai
---
# Debug: Ollama VRAM Thrashing

## Symptoms
- First query after idle is slow (10-30s instead of 1-3s)
- GPU VRAM usage drops to 0 between queries
- Model reloads visible in Ollama logs

## Root Cause
Ollama default `keep_alive` is 5 minutes. After 5m of no queries, it unloads the model from VRAM. Next query triggers full reload.

## Fix
```python
# In Ollama config or API call
keep_alive = "60m"  # Keep model in VRAM for 60 minutes
num_gpu = -1         # Offload ALL layers to GPU (auto-detect)
```

## Prevention
- Set `keep_alive` to match your usage pattern (60m for active use)
- Monitor VRAM with `nvidia-smi` to confirm model stays loaded
- For 24/7 assistants, use `keep_alive: -1` (never unload)
