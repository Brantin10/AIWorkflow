# Project Memory

## Learning_path_2 (Clean Rewrite)
- Location: `C:\Users\oliver\Desktop\Learning_path_2`
- Original: `C:\Users\oliver\Desktop\Learning_path` (messy, kept for reference)
- Android app: `C:\Users\oliver\Desktop\MyFutureCarrer-master` (Kotlin + Firebase)

## Architecture
- `src/api/` — FastAPI server (app.py, routes.py, schemas.py, profile_mapper.py)
- `src/generation/` — Model inference (model.py, pipeline.py, prompts.py)
- `src/generation/focus_plan.py`, `validation.py` — exist but unused now (were for per-step generation)
- `src/evaluation/` — Scoring (scoring.py, taxonomy.py, parsing.py)
- `src/enrichment/` — YouTube resources (youtube.py) — career-generic, not trades-only
- `src/careers/` — Career catalog + fuzzy matching (catalog.py, matcher.py)
- `src/config.py` — Central config
- `data/adapter/` — Phi-3 QLoRA adapter (~100MB)
- `data/careers.jsonl` — 185 trained careers from training pairs

## Key Decisions
- **Full-path generation** — model outputs ALL 12 steps in one JSON blob (matches training format)
- Per-step generation was ABANDONED because model was trained on full-path prompts, not individual steps
- The training format uses `### OUTPUT_JSON` marker and expects complete JSON response
- All heavy imports (torch, transformers, peft) are lazy/deferred in model.py
- No sys.path hacking — proper package structure with `src.` imports
- Training tools excluded from project (user trains separately)
- YouTube enricher is career-family-aware (web, mobile, trades, software, generic)
- career_family() checks trades BEFORE software to avoid "ai" substring in "maintenance"
- Short tokens (ai, it, ml) use word-boundary matching not substring

## Working Setup (CONFIRMED)
- **Python 3.12** (3.14 doesn't have torch wheels)
- **torch 2.8.0+cu128** — REQUIRED for RTX 5070 Ti (sm_120 / Blackwell)
  - torch 2.6.0+cu124: FAILS — no sm_120 kernel images
  - torch 2.10.0+cu128/nightly: had generation issues
  - torch 2.8.0+cu128: WORKS — includes sm_120 in arch list
- **transformers 4.57.6** (must be <5.0 — v5 breaks Phi-3 rope_scaling)
- **peft 0.18.1, accelerate 1.12.0**
- **use_cache=False** required (DynamicCache bug with use_cache=True + peft)
- RTX 5070 Ti GPU, ~8 seconds to load model
- Generation takes ~4.5 minutes for full 12-step path (~3985 chars output)

## Known Quality Issues
- Model generates repetitive titles (e.g., "Build the core foundations needed for Web Developer" repeated)
- This is a training data quality issue, not infrastructure — can be fixed by retraining adapter
- Evaluation scores typically around 3.3/5 — room for improvement with better training data

## API Endpoints
- `POST /api/v1/learning-path` — Generate learning path
  - Body: `{"user_uid": "...", "target_career": "...", "age": 22, "education": "...", "skills": "...", "current_job": "..."}`
- `GET /api/v1/health` — Health check
- `GET /docs` — Swagger UI

## Launch Commands
```bash
cd C:\Users\oliver\Desktop\Learning_path_2
.venv\Scripts\python.exe -m src.api.app
```

## Venvs
- `Learning_path_2/.venv` — Python 3.12 with torch 2.8.0+cu128, transformers, peft, fastapi, etc.
- `Learning_path/.venv312` — old project venv (problematic nightly torch)
