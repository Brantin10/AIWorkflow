---
title: "Electron Context Isolation Error"
created: "2026-03-18"
updated: "2026-03-18"
tags: [playbook, electron, javascript, security, debugging]
status: active
type: playbook
usefulness: high
read-count: 0
source-project: Orchestrator
---

# Electron Context Isolation Error

## Symptom
```
Uncaught ReferenceError: require is not defined
```
Or renderer cannot access Node.js APIs (fs, path, etc.).

## Root Cause
With `contextIsolation: true` (default in Electron 12+), the renderer runs in a sandboxed context. Direct `require()` and Node.js APIs are blocked.

## Fix
Use `contextBridge` in preload.js to expose only what you need:

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  getData: () => ipcRenderer.invoke('get-data'),
  saveData: (data) => ipcRenderer.invoke('save-data', data),
});
```

```javascript
// main.js — BrowserWindow config
new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
    contextIsolation: true,   // REQUIRED for security
    nodeIntegration: false,    // REQUIRED for security
  }
});
```

```javascript
// renderer (app.js)
const data = await window.api.getData();  // Works!
const fs = require('fs');                  // ERROR — intentionally blocked
```

## Common Mistakes
1. **Setting `nodeIntegration: true`** — Security risk, allows XSS to access filesystem
2. **Forgetting to register handlers in main.js** — `invoke()` hangs forever if no `handle()` exists
3. **Using `send()` where `invoke()` is needed** — `send()` is fire-and-forget, `invoke()` returns a Promise
4. **CSP blocking inline scripts** — Add `'unsafe-inline'` to style-src only, never script-src
