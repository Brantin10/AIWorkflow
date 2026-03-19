---
title: "Research: Obsidian + Claude Code Integration Best Practices"
created: "2026-03-19"
updated: "2026-03-19"
tags: [research, obsidian, claude-code, integration, vault, mcp, best-practices]
status: active
type: research
usefulness: high
read-count: 0
---

# Research: Obsidian + Claude Code Integration Best Practices

How to structure an Obsidian vault for maximum effectiveness with Claude Code and other AI agents.

## Access Methods

### 1. MCP Plugin (Port 22360)
- Obsidian MCP plugin exposes vault via WebSocket
- Enables: file read/write, search, active file info, workspace context
- Best for: real-time vault interaction during Claude Code sessions
- Requires: Obsidian running with MCP plugin enabled
- Auto-discovered by Claude Code when available

### 2. Orchestrator REST API (Port 3211)
- Custom Electron app with Express server
- Endpoints: `/api/vault/search`, `/api/vault/read`, `/api/vault/write`, `/api/vault/bundle`
- Best for: programmatic access, context bundles, project scaffolding
- Requires: Orchestrator app running

### 3. Direct File Access
- Vault is just a folder of `.md` files
- Read/write with any language's file I/O
- Best for: simple operations, scripts, CI/CD
- Requires: nothing (always available)

## Vault Structure for AI Orientation

Structure the vault so AI agents can quickly orient themselves:

```
00-Inbox/              — Unprocessed, triage needed
01-Projects/           — Project overviews (AI reads these first)
02-Patterns/           — Reusable solutions (AI references during coding)
03-Skeletons/          — Code templates with {{variables}}
04-ADRs/               — Architecture decisions (AI understands "why")
05-Debug-Playbooks/    — Step-by-step fixes (AI follows during debugging)
06-Research/           — Background knowledge (AI uses for context)
07-Skills/             — AI prompt templates (.md files as prompts)
08-Archive/            — Old notes (AI ignores unless searching)
09-ScriptVault/        — App-specific operational data
```

### Key Principle: Structure for AI, Not Just Humans

Humans navigate by memory and spatial awareness. AI agents navigate by:
1. **Folder names** — Numbered prefixes create scannable hierarchy
2. **YAML frontmatter** — Machine-queryable metadata
3. **File names** — Descriptive, kebab-case names AI can filter with glob patterns
4. **Wiki-links** — `[[note-name]]` creates navigable knowledge graph

## YAML Frontmatter as Machine-Queryable Metadata

Every note should have structured frontmatter:

```yaml
---
title: "Human-readable title"
created: "2026-03-19"
updated: "2026-03-19"
tags: [tag1, tag2, tag3]
status: active          # active | archived | draft
type: pattern           # pattern | adr | playbook | project | research
usefulness: high        # high | medium | low
read-count: 0           # Track how often AI reads this
---
```

### Why Each Field Matters

| Field | AI Use |
|-------|--------|
| `title` | Display in search results, context bundles |
| `tags` | Filter notes by topic, technology, domain |
| `status` | Skip archived notes, prioritize active ones |
| `type` | Know what kind of note it is (pattern = how-to, ADR = why, playbook = debug) |
| `usefulness` | Prioritize high-usefulness notes in context windows |
| `read-count` | Track which notes are actually being used; prune unused ones |

## Tiered Memory Model

Structure vault content by persistence level:

### Tier 1: Evergreen (Permanent)
- Patterns, ADRs, playbooks
- Rarely change, always relevant
- AI should cache these aggressively
- Examples: `02-Patterns/`, `04-ADRs/`, `05-Debug-Playbooks/`

### Tier 2: Project (Active Lifecycle)
- Project overviews, research, current work
- Change frequently during active development
- AI should re-read each session
- Examples: `01-Projects/`, `06-Research/`

### Tier 3: Ephemeral (Daily/Session)
- Inbox items, scratch notes, logs
- May be processed and archived or deleted
- AI should not rely on these persisting
- Examples: `00-Inbox/`

## Wiki-Links as Knowledge Graph

Use `[[wiki-links]]` to connect related notes:

```markdown
# LoRA Fine-Tuning Pattern

This pattern is used in [[scriptvault]] for brand-voice generation.
See [[adr-multi-model-orchestration]] for why we chose local LoRA
over cloud APIs.

If training crashes, see [[lora-training-gpu-oom-fix]].
```

Benefits:
- AI can follow links to gather related context
- Obsidian graph view shows relationships visually
- Backlinks reveal unexpected connections

## Vault as Cross-Session, Cross-Provider Memory

### The Key Insight
AI sessions are ephemeral. Vaults are persistent. The vault bridges the gap.

```
Session 1 (Claude Code)
  → Discovers pattern
  → Writes to vault
  → Session ends

Session 2 (Claude Code, different day)
  → Reads vault
  → Has all knowledge from Session 1
  → Builds on it

Session 3 (ChatGPT via Proxima)
  → Reads same vault
  → Has knowledge from Sessions 1 & 2
  → Different model, same memory
```

### Cross-Provider Compatibility
- Vault notes are plain Markdown — any AI can read them
- YAML frontmatter is universally parseable
- No proprietary format lock-in
- Works with Claude, ChatGPT, Gemini, local models, future models

## .md Skill Files as Reusable AI Prompts

Store AI prompts as vault notes with frontmatter metadata:

```markdown
---
title: "Company Overview Intel"
skill_category: intel
output_fields: [company_name, industry, size]
model: chatgpt
---

You are a B2B researcher. Analyze {{url}} and return JSON with...
```

Benefits:
- Version-controlled prompts (git tracks changes)
- Human-editable in Obsidian (no need to touch code)
- Machine-discoverable (scan folder, parse frontmatter)
- Adding new skills = adding a file, zero code changes
- See [[multi-skill-md-pipeline-pattern]] for implementation details

## CLAUDE.md as Session Bootstrap

Every project should have a `CLAUDE.md` at the root that tells Claude Code:
1. What this project is
2. Where things live
3. What conventions to follow
4. What vault mode to use

This file is read automatically at session start, giving Claude Code immediate context without manual explanation.

## Practical Tips

1. **Read project note first** — Always start a session by reading the project's note from `01-Projects/`
2. **Update notes after learning** — When you solve a problem, write it to the vault before the session ends
3. **Use frontmatter consistently** — Skip it once and search breaks for that note
4. **Keep notes atomic** — One topic per note; easier for AI to find and reference
5. **Archive, do not delete** — Move old notes to `08-Archive/`; they might be useful later
6. **Tag generously** — Tags cost nothing and make search much more powerful
7. **Review read-count** — Notes with zero reads after months can be archived
