---
title: "Obsidian Vault Index Cache Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, javascript, obsidian, caching, performance]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: Orchestrator
---

# Obsidian Vault Index Cache Pattern

## Problem
Searching an Obsidian vault with 100+ markdown notes requires reading and parsing every file. Doing this per-search is slow.

## Solution
In-memory index cache with TTL-based invalidation. Parse all notes once, cache frontmatter + lowercase content, rebuild only when stale or after writes.

## Code

```javascript
const matter = require('gray-matter');

let _indexCache = null;
const INDEX_TTL = 30000; // 30 seconds

function getIndex() {
  const now = Date.now();
  if (_indexCache && (now - _indexCache.builtAt) < INDEX_TTL)
    return _indexCache.entries;
  return rebuildIndex();
}

function rebuildIndex() {
  const files = getAllMdFiles(VAULT_PATH);
  const entries = files.map(f => {
    const raw = fs.readFileSync(f, 'utf-8');
    const parsed = matter(raw);
    return {
      path: path.relative(VAULT_PATH, f).replace(/\/g, '/'),
      frontmatter: parsed.data,
      title: parsed.data.title || path.basename(f, '.md'),
      type: parsed.data.type || '',
      tags: parsed.data.tags || [],
      content: raw.toLowerCase(), // pre-lowercased for search
      rawContent: parsed.content.trim(),
      mtime: fs.statSync(f).mtimeMs
    };
  });
  _indexCache = { entries, builtAt: Date.now() };
  return entries;
}

function invalidateIndex() { _indexCache = null; }

function searchNotes(query) {
  const q = query.toLowerCase();
  return getIndex()
    .filter(entry => entry.content.includes(q))
    .map(entry => ({
      path: entry.path,
      title: entry.title,
      snippet: extractSnippet(entry.content, q)
    }));
}
```

## Access Tracking Add-on

```javascript
let _accessLog = {};

function trackAccess(notePath) {
  const now = new Date().toISOString();
  if (!_accessLog[notePath]) {
    _accessLog[notePath] = { reads: 0, firstRead: now, lastRead: now };
  }
  _accessLog[notePath].reads++;
  _accessLog[notePath].lastRead = now;
  // Debounced save to disk every 10 seconds
}
```

## Key Points
- 30s TTL avoids stale reads while preventing rebuild on every search
- `invalidateIndex()` called after every write operation
- Pre-lowercase content avoids repeated `.toLowerCase()` per search
- Access tracking identifies unused notes for archival
- gray-matter parses YAML frontmatter from markdown files
