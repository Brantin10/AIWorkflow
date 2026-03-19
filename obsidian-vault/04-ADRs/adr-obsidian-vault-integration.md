---
title: "ADR: Obsidian Vault as Knowledge Base"
created: "2026-03-18"
updated: "2026-03-18"
tags: [adr, architecture, obsidian, knowledge-management]
status: active
type: adr
usefulness: high
read-count: 0
source-project: Orchestrator
---

# ADR: Obsidian Vault as Knowledge Base

## Status
Accepted

## Context
AI-assisted development generates reusable knowledge (patterns, ADRs, debug playbooks, research). Need a persistent, searchable knowledge base that:
1. Is human-readable and editable
2. Supports structured metadata (frontmatter)
3. Can be searched programmatically
4. Works offline
5. Scales to hundreds of notes

## Decision
Use an Obsidian vault (`C:\Users\oliver\Obsidian\DevVault`) as the knowledge store. Parse notes with `gray-matter` for YAML frontmatter. Build an in-memory index cache for fast search. Expose via REST API (port 3211) and Electron IPC.

### Folder Structure
```
01-Projects/     — Project overview notes
02-Patterns/     — Reusable coding patterns
03-Skeletons/    — Starter templates
04-ADRs/         — Architecture decisions
05-Debug-Playbooks/ — Bug solutions
06-Research/     — Technical research
07-Skills/       — Skill definitions
08-Archive/      — Stale notes
```

### Access Methods
- **Orchestrator UI:** Electron IPC (vault-list-notes, vault-search, etc.)
- **JARVIS:** REST API (`curl http://localhost:3211/api/vault/...`)
- **Claude Code:** Direct file reads from vault path
- **Human:** Obsidian desktop app

## Consequences
### Positive
- Notes are plain markdown — portable, version-controllable, human-editable
- Frontmatter enables typed queries (type, tags, usefulness)
- Index cache (30s TTL) makes search fast without a database
- Context bundles auto-assemble relevant knowledge per project
- Access tracking identifies unused notes for archival

### Negative
- No full-text search index (substring matching only)
- Index rebuild scans all files (scales linearly with vault size)
- No concurrent write protection (single-writer assumption)
