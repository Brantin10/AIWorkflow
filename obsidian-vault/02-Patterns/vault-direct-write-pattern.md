---
title: "Vault Direct Write Pattern"
created: "2026-03-19"
updated: "2026-03-19"
tags: [pattern, vault, obsidian, file-write, python]
status: active
type: pattern
usefulness: high
read-count: 0
---

# Vault Direct Write Pattern

How to write notes to an Obsidian vault from Python (or any language) without depending on HTTP APIs or Obsidian being running.

## Core Approach

Obsidian vaults are just folders of `.md` files. Write directly to the filesystem using pathlib.

```python
from pathlib import Path
import yaml
from datetime import date

VAULT_PATH = Path("C:/Users/oliver/Obsidian/DevVault")

def write_vault_note(
    relative_path: str,
    title: str,
    content: str,
    tags: list[str] = None,
    extra_frontmatter: dict = None
):
    """Write a markdown note to the Obsidian vault."""
    full_path = VAULT_PATH / relative_path

    # Create parent directories if needed
    full_path.parent.mkdir(parents=True, exist_ok=True)

    # Build frontmatter
    frontmatter = {
        "title": title,
        "created": str(date.today()),
        "updated": str(date.today()),
        "tags": tags or [],
    }
    if extra_frontmatter:
        frontmatter.update(extra_frontmatter)

    # Write file
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    full_content = f"---\n{yaml_str}---\n\n{content}"

    full_path.write_text(full_content, encoding="utf-8")
    return full_path
```

## Directory Structure Convention

All ScriptVault notes live under `09-ScriptVault/` for isolation:

```
C:/Users/oliver/Obsidian/DevVault/
├── 01-Projects/          # Project overviews (shared)
├── 02-Patterns/          # Reusable patterns (shared)
├── 09-ScriptVault/       # ScriptVault-specific notes
│   ├── campaigns/        # Campaign summaries
│   ├── skeletons/        # Template documentation
│   └── winning/          # High-performing scripts
```

## Example: Writing a Campaign Summary

```python
def sync_campaign_to_vault(campaign: dict):
    """Sync a campaign's current state to a vault note."""
    slug = campaign["name"].lower().replace(" ", "-")
    path = f"09-ScriptVault/campaigns/{slug}.md"

    content = f"""# {campaign['name']}

## Status: {campaign['status']}

**Created:** {campaign['created_at']}
**Scripts:** {campaign['script_count']}
**Total Sent:** {campaign['total_sent']}

## Performance
- Open Rate: {campaign['open_rate']}%
- Reply Rate: {campaign['reply_rate']}%
- Meeting Rate: {campaign['meeting_rate']}%

## Scripts
"""
    for script in campaign.get("scripts", []):
        content += f"- **{script['name']}** (Score: {script['score']})\n"

    write_vault_note(
        relative_path=path,
        title=campaign["name"],
        content=content,
        tags=["campaign", "scriptvault", campaign["status"]],
        extra_frontmatter={
            "type": "campaign",
            "source": "scriptvault",
            "campaign_id": campaign["id"],
        }
    )
```

## Obsidian Picks Up Changes Automatically

- Obsidian watches the vault folder for filesystem changes
- New/modified files appear in the file explorer within seconds
- The Orchestrator's index cache picks up changes within ~30 seconds
- No need to restart Obsidian or manually refresh

## Key Rules

1. **`mkdir(parents=True, exist_ok=True)`** — Always create parent dirs; the folder might not exist yet
2. **UTF-8 encoding** — Always specify `encoding="utf-8"` for international characters
3. **YAML frontmatter** — Use the `yaml` library, not string concatenation (handles escaping)
4. **Slugify filenames** — Replace spaces with hyphens, lowercase, strip special characters
5. **No dependency on Orchestrator** — Direct file writes work even if Orchestrator is not running
6. **Idempotent writes** — Overwriting an existing file is fine; Obsidian handles it gracefully

## Comparison with Alternatives

| Approach | Pros | Cons |
|----------|------|------|
| **Direct file write** | No dependencies, works offline, fastest | No validation, no conflict detection |
| **Orchestrator REST API** | Validation, search, bundling | Requires Orchestrator running on port 3211 |
| **Obsidian MCP (port 22360)** | Full vault access, search | Requires Obsidian + MCP plugin running |

For ScriptVault, direct file write was chosen because:
- ScriptVault might run when Orchestrator is not open
- Writes are simple (create/overwrite), no complex queries needed
- Vault sync is a nice-to-have, not a critical dependency
