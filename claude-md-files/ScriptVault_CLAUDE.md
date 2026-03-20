# CLAUDE.md — ScriptVault

## What This Is
B2B sales script intelligence platform. AI generates personalized script GUIDES (not robotic templates) that reps adapt to their own voice. Core philosophy: **out-frame the status quo** — lead with cost of inaction, not features.

## Architecture

### Backend (FastAPI, port 8000)
```
backend/app/
├── api/v1/          # 18 routers (scripts, campaigns, ai, training, vault, etc.)
├── services/        # 24 services (scoring, rewrite, synthetic_data, etc.)
├── models/          # 11 SQLAlchemy models (script, campaign, client, etc.)
├── schemas/         # Pydantic validation
├── parsers/         # CSV, JSON, XLSX, DOCX, TXT, MD importers
└── core/security.py # JWT auth
```
- DB: SQLite at `backend/storage/scriptvault.db`
- Start: `cd backend && python -m uvicorn app.main:app --reload --port 8000`

### Frontend (React 19 + Vite, port 5173)
```
frontend/src/
├── pages/           # 17 pages (Dashboard, AIStudio, Optimizer, etc.)
├── components/      # layout/, common/, scripts/, campaigns/, ai/
├── api/             # Axios client modules
└── context/         # AuthContext (JWT state)
```
- Start: `cd frontend && npm run dev`

### Training Pipeline (D:/lora_training/)
- QLoRA fine-tuned Mistral-7B on 2,290 training pairs
- Adapter: `D:/lora_training/qlora-momentum-ai/`
- Data: `D:/lora_training/training_data/combined_training_data.jsonl`
- Venv: `D:/lora_training/venv/` (PyTorch + CUDA 12.8)

## Core Philosophy (EMBED IN ALL AI PROMPTS)
```
Your core philosophy: out-frame the status quo. The prospect compares
you to the comfort of not deciding — make doing nothing feel dangerous.
Lead with cost of inaction, not features.
```

## 9-Metric Scoring Engine
Every generated script is scored 0-5 on:
1. clarity, 2. personalization, 3. structure, 4. urgency,
5. social_proof, 6. call_to_action, 7. relevance,
8. conciseness, 9. status_quo_framing

Quality gate: overall score > 3.5 to pass. Implemented in `scoring_service.py`.

## Key Services
| Service | Purpose |
|---------|---------|
| `scoring_service.py` | 9-metric script scoring |
| `ai_service.py` | ChatGPT generation via Proxima |
| `synthetic_data_service.py` | Training data generation |
| `rewrite_service.py` | Script optimization |
| `vault_read_service.py` | Obsidian vault context |
| `skeleton_service.py` | Script template management |

## AI Integration
- All AI calls go through Proxima: `http://localhost:3210/v1/chat/completions`
- Models: `chatgpt` (default), `perplexity` (research), `claude`, `gemini`
- Timeout: MINIMUM 120s (Proxima can be slow)
- Always include philosophy block in system prompts
- Always strip markdown fences from AI responses

## Industries Supported
SaaS, Healthcare, Finance, Consulting, Technology, Real Estate, Insurance, Marketing, Manufacturing, Logistics

## Script Types
cold-email, follow-up, linkedin, objection-handler, referral

## Don't
- Generate scripts without the philosophy block in the prompt
- Skip scoring after generation
- Use "we/our" in scripts — Oliver is a solo builder
- Modify scoring weights without validating against existing data
- Call Proxima with < 120s timeout
