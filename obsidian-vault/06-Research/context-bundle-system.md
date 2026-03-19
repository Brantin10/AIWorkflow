---
title: "Context Bundle System for AI-Assisted Development"
created: "2026-03-18"
updated: "2026-03-18"
tags: [research, ai, knowledge-management, context, orchestrator]
status: active
type: research
usefulness: high
read-count: 0
source-project: Orchestrator
---

# Context Bundle System for AI-Assisted Development

## Overview
When dispatching work to AI tools (Claude Code, Cursor), they need relevant context: project overview, architecture decisions, coding patterns, known bugs. The context bundle system auto-assembles this from the Obsidian vault.

## How It Works
1. Read the project note from `01-Projects/{slug}.md`
2. Extract the tech stack from frontmatter
3. Find matching notes by stack keywords:
   - ADRs tagged with relevant stack technologies
   - Skeletons matching the stack
   - Research notes under the project folder
   - Debug playbooks for the project's tech
4. Assemble into a single markdown document
5. Write to `01-Projects/bundles/bundle-{slug}.md` in the vault
6. Optionally write to the project's `.ai-hub/vault-context.md` for AI tools

## Bundle Structure
```markdown
# Context Bundle: MyProject

## Project Overview
[from project note]

## Relevant Architecture Decisions
[matched ADRs]

## Applicable Skeletons
[matched skeletons]

## Research
[project-specific research]

## Debug Playbooks
[matched playbooks]
```

## Matching Logic
```javascript
// Match ADRs by project name or stack keywords
const matchingADRs = allADRs.filter(adr => {
  const adrProject = adr.frontmatter.project?.toLowerCase();
  return adrProject === projectName.toLowerCase() ||
    stackKeywords.some(kw => adr.frontmatter.tags?.some(t => t.includes(kw)));
});
```

## Key Findings
- Stack keywords extracted by splitting on `+`, `,`, `&` separators
- Bundle generation takes <100ms for a vault with 100 notes
- Writing to `.ai-hub/vault-context.md` makes context available to CLAUDE.md
- Regenerate bundles when vault notes change (not automatic — triggered manually)
- Bundles average 2-5KB — well within AI context windows
