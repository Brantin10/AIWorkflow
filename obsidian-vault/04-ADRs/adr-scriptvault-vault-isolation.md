---
title: "ADR: ScriptVault Vault Isolation in 09-ScriptVault/"
created: "2026-03-19"
updated: "2026-03-19"
tags: [adr, scriptvault, vault, isolation, architecture]
status: active
type: adr
usefulness: high
read-count: 0
---

# ADR: ScriptVault Vault Isolation

## Status
Accepted

## Context

Multiple applications share the same Obsidian vault (`C:/Users/oliver/Obsidian/DevVault/`):
- **Orchestrator** — AI project management dashboard, uses vault for project bundles, patterns, ADRs
- **JARVIS** — Personal AI assistant, uses vault for memory and context
- **ScriptVault** — Sales script platform, syncs campaigns, scripts, and intel to vault

ScriptVault needs to write notes to the vault for cross-session memory and human review. But ScriptVault notes (campaign summaries, winning scripts, intel reports) are fundamentally different from development notes (patterns, ADRs, debug playbooks).

## Decision

ScriptVault writes all its notes under `09-ScriptVault/` — a dedicated top-level folder in the vault.

### Folder Assignment Convention

```
00-Inbox/          — Unprocessed notes
01-Projects/       — Project overviews (shared, all apps)
02-Patterns/       — Reusable patterns (shared)
03-Skeletons/      — Code skeletons (Orchestrator)
04-ADRs/           — Architecture decisions (shared)
05-Debug-Playbooks/ — Debug guides (shared)
06-Research/       — Research notes (shared)
07-Skills/         — AI skill prompts (ScriptVault intel pipeline)
08-Archive/        — Archived notes
09-ScriptVault/    — ScriptVault-specific operational data
```

### Filtering in Orchestrator

Orchestrator's `generateContextBundle` function filters by source to prevent ScriptVault notes from polluting dev project bundles:

```javascript
// In lib/vault.js
function generateContextBundle(projectName, options = {}) {
    const notes = getAllNotes();
    const filtered = notes.filter(note => {
        // Exclude ScriptVault operational notes from dev bundles
        if (note.frontmatter?.source === 'scriptvault') return false;
        if (note.path.startsWith('09-ScriptVault/')) return false;
        // ... other filters
        return true;
    });
    return buildBundle(filtered, projectName);
}
```

### ScriptVault Frontmatter Convention

All ScriptVault notes include `source: scriptvault` in frontmatter:

```yaml
---
title: "Q1 Enterprise Campaign"
source: scriptvault
type: campaign
campaign_id: 42
---
```

## Consequences

### Positive
- **No interference**: ScriptVault campaign data never appears in Orchestrator dev bundles
- **Safe coexistence**: Multiple apps can write to the vault simultaneously
- **Still searchable**: ScriptVault notes are findable via vault-wide search when needed
- **Human-browsable**: Oliver can open `09-ScriptVault/` in Obsidian and review campaigns
- **Easy cleanup**: Deleting all ScriptVault data = delete one folder

### Negative
- **Convention-based**: Relies on apps following the folder convention; no enforcement
- **Frontmatter duplication**: Both folder path AND frontmatter `source` field used for filtering (belt and suspenders)

### Neutral
- Shared folders (01-Projects, 02-Patterns, 04-ADRs) can contain notes about ScriptVault as a project — that is intentional. The isolation only applies to ScriptVault's operational data (campaigns, scripts, intel).

## Alternatives Considered

### Separate Vault
- Rejected: Obsidian handles one vault at a time well, multiple vaults add friction
- Cross-vault linking is not supported

### Tag-Based Filtering Only
- Rejected: Tags can be forgotten, folder-based isolation is more reliable
- Tags used as secondary filter, not primary

### Database-Only Storage
- Rejected: Vault notes provide human-readable review and cross-session memory
- SQLite is the source of truth; vault is a readable mirror
