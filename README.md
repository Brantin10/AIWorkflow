# AIWorkflow — Oliver's Claude Code + Obsidian Setup

Portable AI development workflow: Obsidian vault, Claude Code hooks, skills, and configuration.
Clone this on any machine to get the full setup instantly.

## What's Inside

### `claude-config/`
Claude Code hooks and settings that make Claude learn from every session:

- **`hooks/on-session-start.py`** — Loads vault patterns, active projects, and last session context at every session start. Also pulls Orchestrator project context if running.
- **`hooks/on-stop.py`** — Logs every task completion to vault with project name and recent files touched. Also logs to Orchestrator if running.
- **`hooks/on-edit.py`** — Tracks every file Claude modifies with timestamps and `[project]` tags. Also logs to Orchestrator if running.
- **`hooks/orchestrator_client.py`** — Shared helper for Orchestrator REST API (port 3211). All calls are best-effort — gracefully skipped if Orchestrator isn't running.
- **`settings.json`** — Hook wiring config (Windows paths — adjust for Mac)
- **`setup-mac.sh`** — Auto-installer for Mac that fixes all paths

### `claude-md-files/`
Project-specific CLAUDE.md files:
- **`Global_CLAUDE.md`** — Workflow orchestration, core principles, stack, lessons learned. Every Claude Code session reads this.
- **`ScriptVault_CLAUDE.md`** — Architecture, philosophy, scoring engine, API structure for ScriptVault project.
- **`Orchestrator_CLAUDE.md`** — Orchestrator project specifics.

### `claude-skills/`
29 Claude Code skill files (.md) — vault integration, frontend design, code review, debugging, etc.

### `obsidian-vault/`
Obsidian DevVault with 170+ notes: patterns, debug playbooks, ADRs, research, project notes.

## Setup on New Machine

**IMPORTANT FOR CLAUDE:** If you're Claude Code on a new machine, read this section and run the setup. The hooks need paths adjusted for the local OS.

### 1. Clone
```bash
git clone https://github.com/Brantin10/AIWorkflow.git
```

### 2. Install Hooks + Config
```bash
# Mac — run the auto-installer
cd AIWorkflow/claude-config
chmod +x setup-mac.sh
./setup-mac.sh

# Windows — copy manually
mkdir %USERPROFILE%\.claude\hooks
copy claude-config\hooks\* %USERPROFILE%\.claude\hooks\
copy claude-config\settings.json %USERPROFILE%\.claude\settings.json
copy claude-md-files\Global_CLAUDE.md %USERPROFILE%\.claude\CLAUDE.md
```

### 3. Fix Vault Path
The hooks reference the Obsidian vault path. Update `VAULT_PATH` in all hook scripts:
- **Windows:** `C:\Users\oliver\Obsidian\DevVault`
- **Mac:** `~/Obsidian/DevVault` (or wherever your vault lives)

The `setup-mac.sh` script handles this automatically.

### 4. Fix Python Path in settings.json
- **Windows:** `C:/Python314/python.exe`
- **Mac:** `python3`

### 5. Skills
```bash
cp -r claude-skills/* ~/.claude/skills/
```

### 6. Verify
Open Claude Code and check:
- Session start should print "Obsidian Vault Context" with recent patterns
- Edit a file — check `DevVault/01-Projects/claude-code-logs/` for today's change log
- Run `/vault-read` to confirm skill access

## How the Learning Loop Works

```
Session Start → Read vault (patterns, projects, last session)
     ↓
During Work → Every file edit logged to vault with [project] tag
     ↓
Session End → Project name + recent files saved to vault
     ↓
Next Session → Reads all of the above as context
```

Every Claude Code session builds on the last. The vault is the persistent memory.

## Keeping in Sync
After making changes on either machine:
```bash
cd AIWorkflow
git add -A && git commit -m "sync: hooks + config" && git push
```
