---
title: Patterns Index
type: moc
tags:
  - moc
  - pattern
---
# Patterns & Decisions

## Architecture Decisions

```dataview
TABLE status, project, date
FROM #adr
SORT date DESC
```

## Debug Playbooks

```dataview
TABLE category, stack
FROM #debug
SORT file.name ASC
```
