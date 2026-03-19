---
title: Project Index
type: moc
tags:
  - moc
  - project
---
# All Projects

## Active

```dataview
TABLE stack, created, status
FROM #project/active
SORT created DESC
```

## Completed

```dataview
TABLE stack, created
FROM #project/completed
SORT created DESC
```
