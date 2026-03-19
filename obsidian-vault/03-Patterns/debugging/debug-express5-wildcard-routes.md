---
title: "Debug: Express 5 wildcard route syntax change"
type: debug-playbook
category: "api"
stack: "Node.js"
date: "2026-03-18"
tags:
  - debug
  - pattern
  - stack/node
---
# Debug: Express 5 Wildcard Route Syntax

## Symptoms
- `PathError: Missing parameter name at index N` on server start
- Routes with `*` wildcard crash: `app.get('/api/vault/notes/*', ...)`
- Worked in Express 4 but fails in Express 5

## Root Cause
Express 5 uses `path-to-regexp` v8 which removed unnamed wildcards. The `*` syntax is no longer valid.

## Fix
Use query parameters instead of path wildcards:
```javascript
// BAD (Express 5)
app.get('/api/vault/notes/*', (req, res) => { req.params[0] })

// GOOD
app.get('/api/vault/note', (req, res) => { req.query.path })
// Client: /api/vault/note?path=01-Projects/my-project.md
```

Or use named params: `app.get('/api/vault/notes/:folder/:file', ...)`

## Prevention
- Check Express version in package.json before using wildcards
- Prefer query parameters for variable-depth paths
- Test routes on startup (Express 5 throws immediately)
