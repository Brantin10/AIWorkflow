---
title: "ScriptVault x Showcase.ai — Strategic Plan"
created: "2026-03-19"
updated: "2026-03-19"
tags: [project, strategy, showcase-ai, scriptvault, active]
status: active
type: project
usefulness: high
---

# ScriptVault x Showcase.ai — Strategic Plan

## The Mission
Build a self-improving outbound system that turns every campaign into compounding intelligence. Not a script generator — a **predictable, learning revenue engine**.

> "Every campaign permanently improves the system. Competitors reset every time."

Claude Code + Obsidian = institutional memory that no competitor has.

---

## What Showcase.ai Does
- B2B AI lead generation company based in Gothenburg, Sweden
- They build "AI Twins" — personalized outbound sales agents for clients
- Score leads 0-100% compatibility before outreach
- Create tailored scripts per client, per industry, per target
- Revenue model: clients pay for AI-powered outreach at scale

## What They're Missing (Oliver's Opportunity)
1. **No script memory** — winning scripts aren't saved as reusable templates
2. **No feedback loop** — campaign results don't improve future scripts
3. **No per-client voice training** — all AI Twins use the same base model
4. **Manual intel gathering** — prospect research is slow and inconsistent
5. **No A/B testing infrastructure** — can't systematically test script angles
6. **No playbook system** — onboarding new industry clients starts from scratch

---

## What We've Built (Current State)

### Core Platform (ScriptVault)
- **64 API routes**, 12 frontend pages, FastAPI + React
- Full CRUD: scripts, skeletons (templates with {{variables}}), campaigns, outcomes
- Import engine: CSV, JSON, XLSX, DOCX, TXT, MD parsing
- Auto-classification: script type, industry, target role
- Dashboard with performance analytics

### Intelligence Features
| Feature | What It Does | Status |
|---------|-------------|--------|
| Intel Pipeline | Batch website analysis via ChatGPT with 7 custom .md skill prompts | Built |
| A/B Variants | Fork skeletons with named angles, compare success rates | Built |
| Industry Playbooks | Auto-assembled playbooks per industry (top scripts + stats) | Built |
| Compatibility Tracking | Correlate lead compatibility score with reply/meeting rates | Built |
| Script Lab / Optimizer | 8-metric scoring engine + AI variant generation | Built |
| Campaign Memory Vault | Structured vault notes per campaign with learnings | Built |
| Signal Engine | Intent signals auto-trigger playbook + script generation | Built |
| Per-Client LoRA | Fine-tuned model per client for brand-voice generation | Built |
| Intelligence Hub | Structured vault schema for AI consumption | Built |
| Sales AI Factory | 5-stage multi-agent pipeline | Built |

### Obsidian Integration
- Direct filesystem writes to `09-ScriptVault/` (no Orchestrator dependency)
- Skeleton → vault skill note on creation
- Campaign outcome → vault performance note on record
- Winning script → vault pattern when success_rate > 20%
- Isolated from dev vault (Orchestrator skips `09-ScriptVault/` in bundles)

### LoRA Training Pipeline
- Export training data from SQLite → JSONL
- QLoRA fine-tuning on RTX 5070 Ti (Phi-3 base, rank 16, 400 steps)
- Inference with adapter loading
- Evaluation: baseline vs LoRA-generated scoring comparison

---

## Critical Missing Layers (from ChatGPT Review)

### 1. Closed-Loop Revenue Attribution
Currently we track: script → campaign → outcome (reply/meeting).
**Missing:** script → meeting → deal closed → revenue generated.
Add: "This exact message generated X pipeline" tracking.

### 2. Rep-Level Augmentation
Position as "makes your team better" not "replaces your team":
- AI coaching per SDR: "Top 3 improvements based on your last 50 sends"
- Personal performance dashboards per rep
- "You underperform on technical buyers" insights

### 3. Quick Win Features to Build
- **"Rewrite My Campaign" button** — input old campaign, output improved + explanation
- **"Why This Script Will Fail" analyzer** — red flags (no hook, weak CTA, no relevance)
- **Daily "Top Opportunities" digest** — 5 companies to contact today with ready scripts
- **Win/Loss insights dashboard** — "what's working THIS WEEK"
- **1-click personalization layer** — generic script → hyper-specific to company + role

### 4. Positioning Shift
- **From:** "AI script generation platform"
- **To:** "A system that turns outbound into a predictable, compounding revenue engine"
- **vs 11x.ai:** "They send more messages. We make each message smarter."
- **vs Artisan:** "They forget every campaign. We learn from every campaign."

---

## Demo Structure (for non-technical leadership, 10-15 min)
1. **The Problem** (2 min) — "Your outbound is inconsistent and doesn't improve"
2. **Show a REAL bad script** (2 min) — something they recognize
3. **ScriptVault analysis** (3 min) — "Here's why it fails" + scoring
4. **AI-generated improvement** (3 min) — side-by-side comparison
5. **Show data** (3 min) — "This improved reply rate by X%"
6. **The kicker** (2 min) — "Every campaign improves the next one automatically"

---

## Improvement Roadmap

### Phase 1: "Holy Sh*t" Demo (First 2 Weeks)
**Goal:** Prove ScriptVault outperforms current outbound in a measurable way.

**Week 1:**
- [ ] Day 1-3: Import REAL campaigns (2-3 clients, 100-500 past messages + outcomes)
- [ ] Day 3-6: Script quality audit — "Here's why 73% of your scripts underperform"
- [ ] Day 5-7: Generate improved variants of their worst scripts

**Week 2:**
- [ ] Day 8-9: Side-by-side comparison (old vs AI-generated, with scores + explanations)
- [ ] Day 8-14: Micro A/B test — send old scripts vs new scripts, track reply rate
- [ ] Day 14: Present results — even +15-25% lift = massive win

**DO NOT build yet:** Multi-tenant, APIs, white-label. None matters until data proves value.

**Claude Code + Obsidian leverage:**
- Claude Code reads vault playbooks before generating any new script
- Obsidian accumulates industry-specific knowledge with every import
- Patterns emerge automatically: "SaaS cold emails with question openers get 2x replies"

### Phase 2: Automation Layer (Month 1-2)
**Goal:** Reduce manual work in Showcase.ai's daily operations.

- [ ] Auto-script generator — new client → system generates full script library from playbooks + LoRA
- [ ] Signal auto-processor — funding/hiring signals trigger script generation automatically
- [ ] Daily digest — vault generates daily summary of performance, signals, scripts
- [ ] Skeleton auto-rating — after 20+ sends, auto-promote winners to playbooks
- [ ] Dead script detection — flag scripts with <5% success rate after 50+ sends

**Claude Code + Obsidian leverage:**
- Claude Code runs scheduled vault reviews: "which scripts need retiring?"
- Obsidian daily notes create audit trail of all automated actions
- Vault patterns feed back into LoRA retraining data

### Phase 3: Intelligence Multiplier (Month 2-3)
**Goal:** Make the system smarter than any individual sales rep.

- [ ] Cross-client learning — anonymized patterns from Client A improve Client B
- [ ] Objection prediction — based on intel + industry, predict objections before outreach
- [ ] Optimal send timing — track when replies come in, recommend best day/time
- [ ] Competitive intel alerts — monitor competitor websites for changes
- [ ] Multi-channel sequencing — email → LinkedIn → follow-up cadence

**Claude Code + Obsidian leverage:**
- Vault becomes the "institutional brain" — survives employee turnover
- Claude Code searches across all client data (anonymized) for cross-pollination
- Obsidian graph view shows which patterns connect across industries

### Phase 4: Scale & Productize (Month 3-6)
**Goal:** Turn ScriptVault from Oliver's tool into a Showcase.ai product feature.

- [ ] Multi-tenant deployment — each client gets their own ScriptVault instance
- [ ] API integration — ScriptVault API feeds into Showcase.ai's AI Twin infrastructure
- [ ] White-label dashboard — clients see their own performance metrics
- [ ] LoRA-as-a-Service — automated per-client model training pipeline
- [ ] Webhook integrations — CRM events trigger signal processing

---

## Key Automations Claude Code + Obsidian Enable

### 1. Pre-Campaign Research
```
Trigger: New campaign created
→ Claude Code searches vault for industry playbook
→ Reads past campaign notes for that industry
→ Suggests best skeletons based on historical performance
→ Pre-fills target info from intel reports
```

### 2. Post-Campaign Learning
```
Trigger: Campaign reaches 50+ outcomes
→ Claude Code reads campaign vault note
→ Analyzes which scripts/angles performed best
→ Updates industry playbook with new learnings
→ Flags underperforming scripts for review
→ Exports top performers to LoRA training set
```

### 3. Client Onboarding
```
Trigger: New client added
→ Claude Code reads client profile (industry, ICP, brand voice)
→ Searches vault for matching industry playbook
→ Generates initial script library from playbook templates
→ Creates client-specific vault folder
→ Starts LoRA training data collection
```

### 4. Continuous Optimization
```
Trigger: Weekly scheduled task
→ Claude Code reads all campaign notes from past week
→ Identifies top 10 and bottom 10 scripts
→ Generates A/B variants of top performers
→ Archives bottom performers
→ Updates vault benchmarks
→ Triggers LoRA retraining if 50+ new training pairs
```

---

## Competitive Advantages

| Capability | 11x.ai | Artisan | Showcase.ai + ScriptVault |
|-----------|--------|---------|--------------------------|
| Per-client voice training | No | No | Yes (LoRA adapters) |
| Persistent campaign memory | No | No | Yes (Obsidian vault) |
| Multi-model orchestration | No | No | Yes (ChatGPT + Claude + local) |
| Local GPU inference | No | No | Yes (RTX 5070 Ti) |
| Self-improving playbooks | No | No | Yes (vault feedback loop) |
| A/B variant testing | Basic | Basic | Yes (with scoring engine) |
| Custom skill prompts | No | No | Yes (.md skill files) |
| Zero API cost for generation | No | No | Yes (local LoRA) |

---

## Metrics to Track (Speak Sales Language, Not AI Language)

### Revenue Impact (what leadership cares about)
- Pipeline generated (currency)
- Revenue influenced by AI-generated scripts
- Cost per meeting (your system vs manual)

### Outbound Effectiveness
- Reply rate (%) — before vs after
- Positive reply rate (%)
- Meeting booked rate (%)

### Efficiency
- Time to generate campaign (hours → minutes)
- Scripts per SDR per day
- Cost per script (near zero with local LoRA vs API tools)

### The Killer Metric: AI vs Human Baseline Uplift
```
Human scripts:      4.2% reply rate
ScriptVault:        6.8% reply rate
                    → +62% improvement
```
**This single number sells the entire system.**

### Learning System Value
- Performance improvement over time (campaign N vs campaign N+10)
- Playbook accuracy (predicted vs actual success rate)
- Vault knowledge growth (notes per month = compounding intelligence)

---

## Session Log

### 2026-03-19 — Initial Build Session
- Built entire ScriptVault platform from scratch (64 routes, 12 pages)
- Created Obsidian vault integration with direct file writes
- Generated 115 synthetic scripts, 55 skeletons, 203 outcomes
- Built LoRA training pipeline, training on RTX 5070 Ti (400 steps)
- Saved 10 vault learning notes (patterns, ADRs, playbooks, research)
- Researched Showcase.ai competitors and market position
- Key insight: the vault feedback loop is the moat — no competitor has persistent, self-improving knowledge management

_Add new session notes below as work continues._
