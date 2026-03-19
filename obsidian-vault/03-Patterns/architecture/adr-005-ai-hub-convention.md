---
title: "ADR: .ai-hub/ folder convention for multi-AI handoffs"
type: adr
status: accepted
project: "Orchestrator"
date: "2026-03-18"
tags:
  - adr
  - pattern
  - stack/node
---
# ADR: .ai-hub/ Folder Convention

## Context
Projects are worked on by multiple AI tools (Claude Code, Cursor, ChatGPT). Each tool needs context about the project state, and work needs to be handed off between tools.

## Decision
Every project gets a `.ai-hub/` directory with standardized markdown/JSON files:
- `context.md` — Architecture, stack, key decisions
- `tasks.md` — Kanban-style task board (In Progress / Ready / Completed)
- `log.md` — Timestamped activity log with agent names
- `handoff.md` — Structured handoff template (from AI → to AI)
- `plan.md` — Multi-phase execution plan
- `phases.json` — Phase state tracking
- `usage.json` — AI tool usage counter
- `vault-context.md` — Obsidian knowledge bundle

## Consequences
- Language-agnostic (markdown/JSON readable by any AI)
- Survives across tool switches and sessions
- Standardized format enables automated parsing (dashboard)
- CLAUDE.md auto-embeds content from .ai-hub/ files
