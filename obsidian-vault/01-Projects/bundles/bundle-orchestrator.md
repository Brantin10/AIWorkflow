---
title: 'Bundle: Orchestrator'
type: context-bundle
project: Orchestrator
date: '2026-03-19'
tags:
  - bundle
---
# Context Bundle: Orchestrator

## Project Overview

# Orchestrator — Multi-AI Project Management Dashboard

## Overview
Electron desktop app that orchestrates AI-assisted software development. Manages projects with phase-based planning, dispatches work to Claude Code or Cursor, integrates with Obsidian DevVault for knowledge management, and runs a REST API on port 3211 for external tool access (JARVIS, scripts).

## Stack & Tools
- **Runtime:** Electron 35 + Node.js
- **API:** Express 5 (REST on port 3211)
- **Vault:** Obsidian integration via gray-matter (frontmatter parsing)
- **IPC:** Electron contextBridge + ipcMain/ipcRenderer
- **AI Gateway:** Proxima (localhost:3210) for ChatGPT/Perplexity routing
- **Data:** JSON files (projects.json, templates.json, phases.json)

## Architecture
```
main.js              — Electron main process, IPC handlers, API boot
preload.js           — contextBridge API surface (40+ methods)
lib/
  api-server.js      — Express REST API (projects, phases, vault, research)
  vault.js           — Obsidian vault read/write/search/bundle with index cache
  project.js         — Project scaffolding + CLAUDE.md generation
  status.js          — Cross-project status checks
renderer/
  index.html + app.js + styles.css — Frameless dashboard UI
```

## Key Features
- Phase-based project tracking with dispatch to Claude Code / Cursor
- Obsidian vault integration: indexed search, context bundles, access tracking
- REST API for external integrations (JARVIS voice commands)
- Template library for reusable project scaffolds
- Research pipeline via Proxima gateway (ChatGPT + Perplexity)
- Vault health monitoring with staleness + usefulness tracking

## Related Notes
- [[02-Patterns/electron-ipc-context-bridge]]
- [[02-Patterns/obsidian-vault-index-cache]]
- [[02-Patterns/express-rest-api-pattern]]
- [[03-Skeletons/electron-app-skeleton]]
- [[04-ADRs/adr-obsidian-vault-integration]]

## Relevant Architecture Decisions

### ADR: Dual access pattern (Electron IPC + REST API)
# ADR: Dual Access Pattern (Electron IPC + REST API)

## Context
Orchestrator is an Electron app but also needs to be accessible by external tools (JARVIS, scripts, Claude Code).

## Decision
Run Express alongside Electron. Same business logic, two access paths:
- **IPC**: `preload.js` exposes `window.orchestrator.*` for the Electron renderer
- **REST**: Express on port 3211 exposes `/api/*` endpoints for external tools

Both call the same underlying functions (e.g., `lib/vault.js`, `lib/project.js`).

Added `web-bridge.js` that shims IPC calls to REST `fetch()` — same UI works in browser without Electron.

## Consequences
- External tools can `curl http://localhost:3211/api/vault/search?q=react`
- Same UI works in Electron (native) and browser (web preview)
- Claude Code can query the vault via REST during coding sessions
- Trade-off: Two API surfaces to maintain

## Alternatives Considered
- IPC only: External tools can't access
- REST only: No native OS integration (file dialogs, shell commands)

### ADR: .ai-hub/ folder convention for multi-AI handoffs
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

