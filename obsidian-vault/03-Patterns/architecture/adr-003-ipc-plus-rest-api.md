---
title: "ADR: Dual access pattern (Electron IPC + REST API)"
type: adr
status: accepted
project: "Orchestrator"
date: "2026-03-18"
tags:
  - adr
  - pattern
  - stack/node
  - stack/electron
---
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
