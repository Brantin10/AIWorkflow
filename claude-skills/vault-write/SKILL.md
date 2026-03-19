---
name: vault-write
description: Save knowledge back to the Obsidian DevVault. Use after solving hard bugs, making architecture choices, completing significant work, or discovering reusable patterns. Captures architecture decisions, debug playbooks, coding skeletons, and project learnings.
---

# Vault Write

Save knowledge to `C:\Users\oliver\Obsidian\DevVault`

## Via Orchestrator API (when running on port 3211)

```bash
# Create or update a note
curl -X POST http://localhost:3211/api/vault/notes \
  -H "Content-Type: application/json" \
  -d '{
    "path": "03-Patterns/architecture/adr-NNN-title.md",
    "frontmatter": {
      "title": "ADR: Title",
      "type": "adr",
      "status": "accepted",
      "project": "ProjectName",
      "date": "YYYY-MM-DD",
      "tags": ["adr", "pattern", "stack/react"]
    },
    "content": "# ADR: Title\n\n## Context\n...\n\n## Decision\n...\n\n## Consequences\n..."
  }'

# Quick capture to inbox
curl -X POST http://localhost:3211/api/vault/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "Quick note about something important"}'
```

## Via Direct File Write (fallback)

Write `.md` files directly to the vault directory with proper YAML frontmatter.

## What Goes Where

| Knowledge Type | Vault Location | Template |
|---------------|---------------|----------|
| Architecture decisions | `03-Patterns/architecture/adr-NNN-title.md` | type: adr |
| Debug solutions | `03-Patterns/debugging/debug-title.md` | type: debug-playbook |
| Reusable code patterns | `02-Skills/coding-skeletons/skeleton-name.md` | type: skeleton |
| Project learnings | Append to `01-Projects/project-name.md` | - |
| Quick unstructured notes | `00-Inbox/note-title.md` | - |

## Required Frontmatter

Always include these fields:
```yaml
---
title: "Note title"
type: adr | debug-playbook | skill | skeleton | research
date: "YYYY-MM-DD"
tags:
  - relevant-tag
---
```

Add `project: "ProjectName"` and `stack: "React"` when applicable.

## File Naming

- Kebab-case: `adr-001-sqlite-over-postgres.md`
- ADRs: `adr-NNN-short-title.md`
- Debug playbooks: `debug-short-title.md`
- Skeletons: `skeleton-name.md`
