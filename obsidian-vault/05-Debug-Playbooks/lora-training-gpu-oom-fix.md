---
title: "Debug Playbook: LoRA Training GPU OOM and CUBLAS Errors"
created: "2026-03-19"
updated: "2026-03-19"
tags: [playbook, debug, lora, gpu, oom, cuda, cublas, training]
status: active
type: playbook
usefulness: high
read-count: 0
---

# Debug Playbook: LoRA Training GPU OOM and CUBLAS Errors

## Problem 1: CUBLAS_STATUS_INTERNAL_ERROR at Step ~14

### Symptoms
```
RuntimeError: CUDA error: CUBLAS_STATUS_INTERNAL_ERROR when calling
cublasGemmStridedBatchedEx
```
- Training starts fine, runs for 10-15 steps
- Crashes consistently around step 14 (varies slightly)
- GPU memory appears to be within limits on `nvidia-smi`

### Root Cause
LoRA rank 32 with sequence length 2048 exceeds 16GB VRAM even with QLoRA 4-bit quantization. The CUBLAS error is a misleading error message for what is actually an OOM condition during matrix multiplication.

### Fix
Reduce LoRA rank from 32 to 16 and alpha from 64 to 32:

```python
# BEFORE (crashes)
lora_config = LoraConfig(r=32, lora_alpha=64, ...)

# AFTER (stable)
lora_config = LoraConfig(r=16, lora_alpha=32, ...)
```

Also reduce max sequence length from 2048 to 1024:

```python
# BEFORE (crashes)
max_seq_length = 2048

# AFTER (stable)
max_seq_length = 1024
```

### Verification
- Training should run to completion (400+ steps) without CUDA errors
- Monitor with `nvidia-smi -l 5` during training
- VRAM usage should stay under 14GB

---

## Problem 2: CUDA Out of Memory (OOM) During Training

### Symptoms
```
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate XXX MiB
(GPU 0; 16.00 GiB total capacity; XX.XX GiB already allocated)
```

### Root Cause
Combination of factors consuming too much VRAM:
- Large sequence length (2048 tokens)
- Batch size > 1
- High LoRA rank
- Gradient accumulation buffers

### Fix Checklist

1. **Reduce max_seq_length to 1024** (biggest impact)
2. **Set per_device_train_batch_size=1** (mandatory for 16GB)
3. **Use gradient_accumulation_steps=4** (simulates batch_size=4)
4. **Ensure 4-bit quantization is active**:
   ```python
   bnb_config = BitsAndBytesConfig(
       load_in_4bit=True,
       bnb_4bit_quant_type="nf4",
       bnb_4bit_compute_dtype=torch.float16,
       bnb_4bit_use_double_quant=True,  # Extra memory savings
   )
   ```
5. **Disable pin_memory**: `dataloader_pin_memory=False`
6. **Use fp16 not bf16**: RTX 5070 Ti supports both, but fp16 uses less memory

### Nuclear Option
If still OOM after all the above:
```python
# Clear GPU cache before training
import torch
torch.cuda.empty_cache()
import gc
gc.collect()
```

And close all other GPU-using applications (browsers with hardware acceleration, etc.).

---

## Problem 3: HuggingFace Cache Fills C: Drive

### Symptoms
```
OSError: [Errno 28] No space left on device
```
Or download hangs/fails silently.

### Root Cause
The Phi-3 model is ~8.2GB. HuggingFace defaults to caching models in `C:\Users\<user>\.cache\huggingface\`. If C: drive has limited free space, this fails.

### Fix
Redirect HuggingFace cache to D: drive. Set these environment variables BEFORE running any training or inference:

**Option A: System Environment Variables** (permanent)
```
HF_HOME=D:/huggingface_cache
TRANSFORMERS_CACHE=D:/huggingface_cache
```

**Option B: In Python** (per-script)
```python
import os
os.environ["HF_HOME"] = "D:/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "D:/huggingface_cache"
# Must be set BEFORE importing transformers
from transformers import AutoModelForCausalLM
```

**Option C: In .env file**
```
HF_HOME=D:/huggingface_cache
TRANSFORMERS_CACHE=D:/huggingface_cache
```

### Verification
After setting, run:
```python
from huggingface_hub import scan_cache_dir
info = scan_cache_dir("D:/huggingface_cache")
print(f"Cache size: {info.size_on_disk / 1e9:.1f} GB")
```

---

## Problem 4: Training Task Times Out in Claude Code

### Symptoms
- Claude Code background task completes but training was killed
- Output shows training started but no final results
- Checkpoint files exist but are incomplete

### Root Cause
Claude Code background tasks have a timeout. Training runs of 30+ minutes exceed this.

### Fix
Use `nohup` to fully detach the training process:

```bash
nohup python train_lora.py > D:/lora_training/training.log 2>&1 &
echo $!  # Save PID to check later
```

Monitor progress:
```bash
tail -f D:/lora_training/training.log
```

Check if still running:
```bash
nvidia-smi  # Look for python process using GPU
```

---

## Quick Reference: Safe Parameters for RTX 5070 Ti 16GB

```python
# LoRA
r = 16
lora_alpha = 32

# Training
per_device_train_batch_size = 1
gradient_accumulation_steps = 4
max_seq_length = 1024
fp16 = True
dataloader_pin_memory = False

# Storage
HF_HOME = "D:/huggingface_cache"
output_dir = "D:/lora_training/checkpoints"
```
