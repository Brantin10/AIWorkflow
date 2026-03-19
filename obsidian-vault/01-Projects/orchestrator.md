---
title: "Orchestrator"
created: "2026-03-18"
updated: "2026-03-18"
tags: [project, project/active, stack/electron, stack/node, stack/express, stack/obsidian]
status: active
type: project
usefulness: high
read-count: 0
---

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
