---
title: "ADR: Multi-Model AI Orchestration"
created: "2026-03-19"
updated: "2026-03-19"
tags: [adr, multi-model, ai, orchestration, chatgpt, claude, lora]
status: active
type: adr
usefulness: high
read-count: 0
---

# ADR: Multi-Model AI Orchestration

## Status
Accepted

## Context

ScriptVault's pipeline involves multiple AI-powered stages:
1. **Research** — Gathering intel on prospects and companies
2. **Analysis** — Understanding pain points, identifying opportunities
3. **Strategy** — Deciding script approach, tone, positioning
4. **Generation** — Writing the actual sales scripts
5. **Scoring** — Evaluating script quality
6. **Optimization** — Improving scripts based on feedback

No single AI model is best at all of these. Each model has strengths and weaknesses, and costs vary dramatically.

## Decision

Use different AI models for different pipeline stages, matched to each model's strengths.

### Model Assignment

| Stage | Model | Why |
|-------|-------|-----|
| **Research & Intel** | ChatGPT (via Proxima) | Best web knowledge, broad training data, good at synthesizing public info |
| **Web Search** | Perplexity (via Proxima) | Real-time web search with citations, current events |
| **Reasoning & Strategy** | Claude Code | Best at complex reasoning, nuanced strategy, code generation |
| **Script Generation** | Local LoRA (Phi-3) | Brand-voice fine-tuned, zero API cost, fully private, fast inference |
| **Scoring** | Deterministic engine | No LLM needed — rule-based scoring is faster, cheaper, and more consistent |
| **Optimization** | ChatGPT or Claude | Needs broad knowledge of what makes good sales copy |

### Communication Between Models

The Obsidian vault serves as shared memory across all models:

```
ChatGPT (research)
    → writes intel to vault (09-ScriptVault/)
        → Claude Code reads intel, plans strategy
            → writes strategy to vault
                → Local LoRA reads strategy, generates scripts
                    → Scoring engine evaluates
                        → Results back to vault
```

No model talks directly to another. The vault is the message bus.

### API Architecture

```
Proxima MCP (localhost:3210)
├── /v1/chat/completions  {model: "chatgpt"}  → ChatGPT
├── /v1/chat/completions  {model: "perplexity"} → Perplexity
└── /v1/new_conversation  → Reset context

Local LoRA (Python process)
├── Load base model + LoRA adapter
├── Generate with custom prompt template
└── Return generated text

Scoring Engine (Python, no API)
├── Rule-based scoring functions
├── Deterministic output
└── Sub-millisecond latency
```

## Consequences

### Positive
- **Best model for each job**: Research quality from ChatGPT, reasoning from Claude, brand-voice from LoRA
- **Cost optimization**: LoRA generation is free after training; scoring is free always
- **Privacy**: Sensitive client data can stay local (LoRA), only public info goes to cloud APIs
- **Resilience**: If one model is down, others still work; pipeline degrades gracefully
- **Upgradeable**: Swap any model without changing the pipeline; just change which model handles which stage

### Negative
- **Complexity**: More moving parts than a single-model approach
- **Latency**: Multiple model calls are slower than one; mitigated by parallelism where possible
- **Context loss**: Models do not share conversation context; vault notes must be explicit

### Neutral
- Vault-as-message-bus means all intermediate results are human-readable and debuggable
- Adding a new model (e.g., Gemini for multimodal analysis) is trivial — just add a new route

## Alternatives Considered

### Single Model (Claude or ChatGPT for Everything)
- Rejected: Too expensive for high-volume generation, no brand-voice fine-tuning possible
- API costs scale linearly with volume; local LoRA has zero marginal cost

### Local Model Only
- Rejected: 3.8B parameter model cannot match ChatGPT's research breadth or Claude's reasoning depth
- Local models excel at narrow, fine-tuned tasks, not general intelligence

### Direct Model-to-Model Communication
- Rejected: Creates tight coupling, debugging is harder, no audit trail
- Vault-as-bus gives full transparency and human-reviewable intermediate steps

## Future Direction

### Per-Client LoRA Adapters
- Train separate LoRA adapters per client's brand voice
- Swap adapters at inference time: same base model, different personality
- Zero additional API cost per client

### AI Factory (End-to-End Automation)
- Orchestrate the full pipeline automatically: signal -> intel -> strategy -> generation -> scoring -> optimization
- Human reviews final output, not intermediate steps
- Vault stores complete audit trail of every decision
