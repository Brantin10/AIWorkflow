---
name: vault-curate
description: Review and curate the Obsidian DevVault. Check vault health, find stale/unrated/never-read notes, rate note usefulness, archive low-value notes, and get performance stats. Use when user asks to clean up the vault, check vault health, review notes, or rate vault content. Also triggers automatically when vault warnings appear.
---

# Vault Curate

Maintain vault quality and performance at `C:\Users\oliver\Obsidian\DevVault`

## Check Vault Health (includes auto-tracked usage data)

```bash
curl -s http://localhost:3211/api/vault/health | jq .
```

Returns:
- `total`: Total note count
- `byType`: Count per note type (project, adr, skeleton, etc.)
- `byUsefulness`: Count by rating (high/medium/low/unrated)
- `stale`: Notes not modified in 90+ days
- `indexStats`: Cache performance (buildMs, note count)
- `warnings`: Auto-generated alerts (vault too large, index slow, unrated notes)
- `access`: Usage tracking data:
  - `topNotes`: Most-read notes (ranked by read count)
  - `neverRead`: Notes that have NEVER been accessed
  - `totalReads`: Total read operations across all notes
  - `trackedNotes`: How many notes have been read at least once

## Auto-Tracking

Every `readNote()` call is automatically logged to `.vault-access-log.json`. This happens when:
- User clicks a note in the vault browser
- Claude Code reads a note via `/vault-read`
- Auto-bundle reads notes to assemble context
- Any API call reads a specific note

No manual tracking needed — usage data accumulates over time.

## Auto-Warnings

The system generates warnings at these thresholds:
- **Yellow (200+ notes)**: "Still fast, but keep an eye on it"
- **Orange (500+ notes)**: "Approaching performance limit"
- **Red (1000+ notes)**: "Searches may be slow — archive unused notes"
- **Index > 500ms**: "Vault is getting heavy"
- **30+ unrated notes**: "Run /vault-curate to review"

## Rate a Note's Usefulness

Add `usefulness: high|medium|low` to frontmatter. Either:
- Edit the file directly in Obsidian
- Or via API:

```bash
curl -s "http://localhost:3211/api/vault/note?path=NOTE_PATH" # read first
# Then update with usefulness field added to frontmatter
curl -X POST http://localhost:3211/api/vault/notes \
  -H "Content-Type: application/json" \
  -d '{"path":"NOTE_PATH","frontmatter":{...existing, "usefulness":"high"},"content":"..."}'
```

## Curate Workflow

1. `curl -s http://localhost:3211/api/vault/health` → check warnings + stats
2. Check `access.neverRead` → these notes may be candidates for archiving
3. Check `access.topNotes` → these are your most valuable notes, rate them `high`
4. Check `stale` → notes untouched for 90+ days, review or archive
5. Review `byUsefulness.unrated` → add ratings to un-rated notes
6. Archive low-value notes to `08-Archive/`

## Performance Guidelines

| Vault Size | Index Build | Action |
|-----------|------------|--------|
| <200 notes | <50ms | No action needed |
| 200-500 | 50-200ms | Index cache keeps it fast |
| 500-1000 | 200-500ms | Archive stale + never-read notes |
| 1000+ | 500ms+ | Aggressive archiving or split vault |

## What to Keep vs Archive

**Keep** (high usefulness) — notes in `access.topNotes`:
- Patterns reused across 2+ projects
- Debug playbooks that saved real debugging time
- Skeletons for stacks you actively use

**Archive** (low usefulness) — notes in `access.neverRead` + `stale`:
- Project notes for finished projects you won't revisit
- Research already embedded in code
- Debug playbooks for one-time bugs
- Templates you never actually used
