---
name: vault-read
description: Read and query the Obsidian DevVault for project context, patterns, skills, and past decisions. Use at project start, before complex tasks, or when user asks about past work, patterns, architecture decisions, or debugging solutions.
---

# Vault Read

Query the Obsidian DevVault at `C:\Users\oliver\Obsidian\DevVault`

The user chooses a vault mode at session start. Use the method matching their choice:

## Method 1: Nexus MCP (when user chose "Nexus")

Use the Nexus MCP tools (2-tool pattern):

```
1. Call getTools to discover available vault operations
2. Call useTools to execute: search, read, list notes, semantic search
```

Nexus provides semantic search (finds notes by meaning, not just keywords), workspace memory, and task management.

## Method 2: Claude MCP (when user chose "Claude MCP")

Auto-discovered via WebSocket (port 22360). Use MCP tools directly:

- `view` — read a vault file
- `create` — create a new note
- `str_replace` — edit a note
- `get_workspace_files` — list vault contents
- `get_current_file` — get active file in Obsidian
- `obsidian_api` — call Obsidian API

No curl needed — these tools appear automatically when Obsidian is running.

## Method 3: Manual / REST API (when user chose "Manual" or Obsidian is closed)

```bash
# Search vault by keyword
curl -s "http://localhost:3211/api/vault/search?q=QUERY"

# Read a specific note
curl -s "http://localhost:3211/api/vault/note?path=01-Projects/project-name.md"

# List notes in a folder, optionally filter by type
curl -s "http://localhost:3211/api/vault/notes?folder=03-Patterns&type=adr"

# Get all notes linked to a project
curl -s "http://localhost:3211/api/vault/bundles?project=ProjectName"

# Vault health + access stats
curl -s "http://localhost:3211/api/vault/health"
```

Or read files directly from `C:\Users\oliver\Obsidian\DevVault/`

## Vault Structure

```
00-Inbox/           Quick captures
01-Projects/        Project notes (one per Orchestrator project)
  bundles/          Context bundles
02-Skills/          Claude skills docs, coding skeletons
03-Patterns/        Architecture decisions (ADRs) + debug playbooks
  architecture/     ADR notes
  debugging/        Debug playbook notes
04-Research/        Research notes per project
05-Learning/        Tutorials, AI experiments
07-Templates/       Note templates
08-Archive/         Archived notes
```

## When to Use

- **Project start**: Check `03-Patterns/architecture/` for relevant ADRs
- **Debugging**: Check `03-Patterns/debugging/` for playbooks matching the error
- **Stack questions**: Search by stack tag (`#stack/react`, `#stack/python`)
- **Project history**: Read `01-Projects/project-name.md` for past learnings
- **Finding skeletons**: Search `02-Skills/coding-skeletons/` for reusable patterns
- **Context bundle**: Read `.ai-hub/vault-context.md` in the project directory
