---
title: "LoRA Fine-Tuning on Consumer GPU Pattern"
created: "2026-03-19"
updated: "2026-03-19"
tags: [pattern, lora, fine-tuning, phi3, qlora, gpu, training]
status: active
type: pattern
usefulness: high
read-count: 0
---

# LoRA Fine-Tuning on Consumer GPU Pattern

How to fine-tune language models on a consumer GPU (RTX 5070 Ti 16GB) using QLoRA. Proven with Phi-3-mini-4k-instruct for brand-voice sales script generation.

## Hardware Requirements

- GPU: NVIDIA RTX 5070 Ti (16GB VRAM) or similar
- RAM: 32GB+ system RAM recommended
- Storage: 20GB+ free on training drive (model + checkpoints)
- CUDA: 12.x with cuDNN

## Model Selection

| Model | Size | Why |
|-------|------|-----|
| `microsoft/Phi-3-mini-4k-instruct` | 3.8B params, ~8.2GB | Best quality-per-VRAM ratio, instruction-tuned, fits in 16GB with QLoRA |

Phi-3 was chosen because:
- 3.8B params fits comfortably in 16GB with 4-bit quantization
- Already instruction-tuned (less fine-tuning needed)
- 4k context window sufficient for sales scripts
- Microsoft-backed, good documentation

## QLoRA Configuration (Proven Working)

```python
from peft import LoraConfig, get_peft_model
from transformers import BitsAndBytesConfig
import torch

# Quantization config — 4-bit is REQUIRED for 16GB VRAM
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# LoRA config — THESE VALUES ARE TESTED AND STABLE
lora_config = LoraConfig(
    r=16,           # Rank 16 — rank 32 CRASHES with CUBLAS error
    lora_alpha=32,  # Alpha = 2x rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```

### Critical Parameters

| Parameter | Safe Value | Dangerous Value | What Happens |
|-----------|-----------|-----------------|-------------|
| `r` (rank) | 16 | 32 | CUBLAS_STATUS_INTERNAL_ERROR at step ~14 |
| `max_seq_length` | 1024 | 2048 | CUDA OOM during training |
| `per_device_train_batch_size` | 1 | 2+ | OOM |
| `gradient_accumulation_steps` | 4 | 1 | Effective batch too small, unstable training |

## Training Data Format

JSONL file with prompt/completion pairs:

```jsonl
{"prompt": "Write a cold outreach email for a SaaS company selling CRM software to a mid-market retail company.", "completion": "Subject: Streamlining Your Customer Relationships...\n\nHi {{first_name}},\n\n..."}
{"prompt": "Write a LinkedIn connection request for a VP of Sales at a fintech startup.", "completion": "Hi {{first_name}}, I noticed your recent post about..."}
```

### Exporting Training Data from SQLite

```python
import sqlite3
import json

def export_training_data(db_path: str, output_path: str, min_score: float = 7.0):
    """Export high-scoring scripts as training data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("""
        SELECT s.prompt, s.content, s.score
        FROM scripts s
        WHERE s.score >= ? AND s.content IS NOT NULL
        ORDER BY s.score DESC
    """, (min_score,))

    with open(output_path, 'w') as f:
        for prompt, content, score in cursor:
            record = {
                "prompt": prompt,
                "completion": content,
                "metadata": {"score": score}  # Optional, stripped before training
            }
            f.write(json.dumps(record) + '\n')

    conn.close()
```

## Training Script

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="D:/lora_training/checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    weight_decay=0.01,
    warmup_steps=50,
    logging_steps=10,
    save_steps=100,
    save_total_limit=3,
    fp16=True,
    max_grad_norm=0.3,
    lr_scheduler_type="cosine",
    report_to="none",       # No W&B or other logging
    dataloader_pin_memory=False,  # Reduces memory
)
```

## Storage Configuration

The HuggingFace model cache is 8.2GB+ and will fill up C: drive. Redirect to D: drive:

```bash
# Set in environment variables (System > Advanced > Environment Variables)
HF_HOME=D:/huggingface_cache
TRANSFORMERS_CACHE=D:/huggingface_cache
```

Or in Python before importing transformers:
```python
import os
os.environ["HF_HOME"] = "D:/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "D:/huggingface_cache"
```

## Running Training

Use `nohup` or background process for long training runs (Claude Code background tasks time out):

```bash
nohup python train_lora.py > D:/lora_training/training.log 2>&1 &
```

### Expected Performance
- ~5 seconds per training step
- 400 steps = ~33 minutes
- 3 epochs over 500 samples = ~375 steps

## Inference with Trained Adapter

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    quantization_config=bnb_config,
    device_map="auto"
)
model = PeftModel.from_pretrained(base_model, "D:/lora_training/checkpoints/checkpoint-400")
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

# Generate
inputs = tokenizer("Write a cold email for...", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Gotchas and Lessons Learned
1. **Always use QLoRA** (4-bit) on 16GB cards — full LoRA will OOM
2. **Rank 16 is the sweet spot** — rank 32 causes CUBLAS crashes even with QLoRA
3. **Max seq length 1024** — 2048 causes OOM during training
4. **HF cache fills C: drive fast** — redirect to D: before first model download
5. **Background the training** — Claude Code tasks time out, use nohup
6. **Save checkpoints frequently** — crashes at step 14 means lost work without checkpoints
7. **gradient_accumulation_steps=4** compensates for batch_size=1
