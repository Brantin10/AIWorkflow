# Orchestrator — AI Project Management Dashboard

## Obsidian Vault Mode

At the START of every project or significant task, ask the user which vault mode to use:

- **Nexus** — Full AI workspace with semantic search, workspace memory, task management, and workflow automation. Use for complex multi-phase projects, research-heavy work, or when persistent workspace context is needed. Nexus tools are available via MCP (getTools/useTools pattern).
- **Claude MCP** — Lightweight vault access via auto-discovered WebSocket (port 22360). File read/write, workspace context, active file info. Use for quick tasks, pattern lookups, or simple context loading.
- **Manual** — REST API (`curl http://localhost:3211/api/vault/...`) or direct file reads from `C:\Users\oliver\Obsidian\DevVault\`. Use when Obsidian is not running.

Remember the user's choice for the session. Do not ask again unless switching projects.

## Vault Location

`C:\Users\oliver\Obsidian\DevVault` — contains project notes, coding skeletons, ADRs, debug playbooks, research, and context bundles.

## Project Structure

- `main.js` — Electron main process + IPC handlers
- `lib/vault.js` — Obsidian vault integration (read/write/search/bundle)
- `lib/api-server.js` — REST API on port 3211 (includes vault endpoints)
- `lib/project.js` — Project scaffolding + CLAUDE.md generation
- `renderer/` — Frontend UI (HTML + JS + CSS)
