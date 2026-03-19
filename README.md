# AIWorkflow — Oliver's Claude Code + Obsidian Setup

Portable AI development workflow: Obsidian vault, Claude Code skills, and configuration.
Clone this on any machine to get the full setup instantly.

## What's Inside

### `obsidian-vault/`
Obsidian DevVault with 170+ notes:
- `01-Projects/` — Project overviews (JARVIS, Orchestrator, AIResume, ScriptVault, etc.)
- `02-Patterns/` — Reusable coding patterns (Electron IPC, FastAPI Auth, Axios Interceptor, etc.)
- `03-Skeletons/` — Starter templates (Electron app, FastAPI+React, Voice Assistant, etc.)
- `04-ADRs/` — Architecture decision records
- `05-Debug-Playbooks/` — Solutions to hard bugs (CORS, SQLite threading, OOM, etc.)
- `06-Research/` — Technical research (Deepgram STT, Model2Vec, Ollama, etc.)
- `07-Skills/` — Vault skill definitions + intel pipeline prompts
- `09-ScriptVault/` — ScriptVault-specific vault data (isolated from dev notes)

### `claude-skills/`
29 Claude Code skill files (.md):
- `audit` — Security vulnerability scanning
- `vault-read` / `vault-write` / `vault-bundle` / `vault-curate` — Obsidian integration
- `frontend-design` — Premium UI generation
- `review` / `review-pr` — Code review
- `debug` — Error investigation
- `test-api` — API endpoint testing
- And more...

### `claude-config/`
Claude Code settings (sanitized).

## Setup on New Machine

### 1. Clone
```bash
git clone https://github.com/Brantin10/AIWorkflow.git
```

### 2. Obsidian Vault
- Install Obsidian from https://obsidian.md
- Open the `obsidian-vault/` folder as a vault
- Enable Community Plugins when prompted

### 3. Claude Code Skills
Copy skills to your Claude config:
```bash
# Mac/Linux
cp -r claude-skills/* ~/.claude/skills/

# Windows
xcopy claude-skills\* %USERPROFILE%\.claude\skills\ /E /Y
```

### 4. Verify
Open Claude Code and run `/audit` or `/vault-read` to confirm skills are loaded.

## Vault Path Configuration
ScriptVault and Orchestrator expect the vault at a specific path. Set the `VAULT_PATH` environment variable:
```bash
# Windows
set VAULT_PATH=C:\Users\oliver\Obsidian\DevVault

# Mac
export VAULT_PATH=~/Obsidian/DevVault
```

## Keeping in Sync
After making changes on either machine, push/pull:
```bash
git add -A && git commit -m "sync vault + skills" && git push
```
