---
title: "ScriptVault — AI Sales Script Platform"
created: "2026-03-19"
updated: "2026-03-19"
tags: [scriptvault, project, sales-ai, lora, fastapi, react]
status: active
type: project
usefulness: high
read-count: 0
---

# ScriptVault

AI-powered sales script management platform with intelligent scoring, optimization, and fine-tuning capabilities. Built for B2B outreach personalization at scale.

**GitHub:** https://github.com/Brantin10/ScriptVault.git
**Stack:** FastAPI + React 19 + SQLite + Obsidian Vault + Proxima/ChatGPT + Phi-3 LoRA

## Architecture

```
Frontend (React 19)  <-->  FastAPI Backend  <-->  SQLite DB
                              |                      |
                        Proxima MCP (port 3210)   Vault Sync
                              |                      |
                        ChatGPT / Perplexity    09-ScriptVault/
                              |
                        Local LoRA (Phi-3)
```

### Backend Structure
- `backend/app/main.py` — FastAPI app entry point
- `backend/app/api/v1/` — Versioned API routes
- `backend/app/services/` — Business logic layer (16 services)
- `backend/app/models/` — SQLAlchemy models (script, campaign, client, skeleton, intel, outcome, signal, etc.)
- `backend/app/schemas/` — Pydantic request/response schemas
- `backend/app/parsers/` — Response parsing utilities
- `backend/app/utils/` — Shared utilities

### Frontend
- React 19 SPA
- Component-based UI for scripts, campaigns, skeletons, intel, playbooks, lab

## Features — Complete Inventory

### Core CRUD
- **Scripts** — Create, read, update, delete sales scripts with rich metadata
- **Skeletons** — Template system with `{{variable}}` placeholders that get filled per-client
- **Campaigns** — Group scripts by outreach campaign with status tracking
- **Outcomes** — Track script performance (sent, opened, replied, meeting booked, closed)

### Intel Pipeline
- Multi-skill `.md` files loaded from vault as AI prompts
- Each skill file has YAML frontmatter (title, output_fields, skill_category)
- Skills scanned from vault folder, no code changes needed to add new ones
- Runs each skill as separate ChatGPT conversation via Proxima
- Results merged into unified intel report per prospect/company
- Service: `intel_service.py`

### A/B Variant System
- Scripts can have multiple variants for testing
- Variant groups track which variants compete against each other
- Outcome tracking per variant for statistical comparison
- Enables data-driven script iteration

### Industry Playbooks
- Pre-built playbook templates per industry vertical
- Contains objection handling, value props, pain points
- Service: `playbook_service.py`

### Compatibility Score Tracking
- Scores how well a script matches a prospect's profile/signals
- Uses deterministic scoring engine (no LLM needed for scoring itself)
- Feeds into optimization recommendations

### Script Lab
- **Scoring Engine** — Deterministic scoring of script quality across multiple dimensions
- **Optimizer** — AI-powered script improvement suggestions
- Services: `scoring_service.py`, `optimizer_service.py`

### LoRA Fine-Tuning Pipeline
- Base model: `microsoft/Phi-3-mini-4k-instruct`
- QLoRA (4-bit quantization) for RTX 5070 Ti 16GB VRAM
- Training data exported from SQLite DB as JSONL prompt/completion pairs
- LoRA rank 16, alpha 32 (rank 32 causes CUBLAS crash)
- Max sequence length 1024 (2048 causes OOM)
- HuggingFace cache on D: drive (model is 8.2GB)
- Checkpoints saved to `D:/lora_training/`
- ~5s/step, 400 steps = ~33 minutes per training run
- Goal: brand-voice generation at zero API cost

### Vault Sync
- Direct file writes to `09-ScriptVault/` in Obsidian vault
- Subfolders: `campaigns/`, `skeletons/`, `winning/`
- Uses pathlib + YAML for file creation (no HTTP dependency)
- Orchestrator picks up changes within 30s via index cache
- Service: `vault_sync_service.py`

### Campaign Memory Vault (Building)
- Persistent memory per campaign across sessions
- Stores what worked, what failed, prospect reactions
- Feeds into future script generation

### Signal Engine (Building)
- Detects buying signals from prospect interactions
- LinkedIn activity, job changes, funding events
- Triggers personalized outreach timing
- Model: `signal.py`

### Per-Client LoRA (Building)
- Fine-tune separate LoRA adapters per client's brand voice
- Swap adapters at inference time for client-specific generation
- Zero additional API cost per client

### AI Factory (Building)
- Orchestrates full pipeline: signal detection -> intel gathering -> script generation -> scoring -> optimization
- End-to-end automation of outreach creation

## Services Inventory

| Service | Purpose |
|---------|---------|
| `ai_service.py` | AI generation orchestration |
| `auth_service.py` | Authentication |
| `campaign_service.py` | Campaign CRUD |
| `campaign_vault_service.py` | Campaign vault sync |
| `classification_service.py` | Script/prospect classification |
| `dashboard_service.py` | Dashboard aggregations |
| `import_service.py` | Bulk data import |
| `intel_service.py` | Intel pipeline with vault skills |
| `optimizer_service.py` | Script optimization |
| `playbook_service.py` | Industry playbooks |
| `scoring_service.py` | Script scoring engine |
| `script_service.py` | Script CRUD |
| `skeleton_service.py` | Skeleton templates |
| `vault_sync_service.py` | Obsidian vault writes |

## Models

| Model | Purpose |
|-------|---------|
| `script.py` | Sales scripts with metadata |
| `campaign.py` | Outreach campaigns |
| `client.py` | Client/prospect profiles |
| `skeleton.py` | Template skeletons |
| `intel.py` | Prospect intelligence |
| `outcome.py` | Script performance tracking |
| `signal.py` | Buying signal detection |
| `import_job.py` | Bulk import tracking |
| `ai_generation.py` | AI generation history |
| `user.py` | User accounts |

## Key Decisions
- SQLite over Postgres: single-user app, simplicity wins
- Vault isolation in `09-ScriptVault/`: prevents interference with other vault apps
- Multiple AI models: ChatGPT for research, Claude for reasoning, local LoRA for generation
- Deterministic scoring: no LLM needed, fast and consistent
- `.md` skill files: new intel skills = just drop a file, zero code changes
