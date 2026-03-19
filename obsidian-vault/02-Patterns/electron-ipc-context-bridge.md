---
title: "Electron IPC Context Bridge Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, electron, javascript, ipc]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: Orchestrator
---

# Electron IPC Context Bridge Pattern

## Problem
Electron apps need secure communication between the renderer (browser) and main (Node.js) processes. Direct `nodeIntegration` is a security risk.

## Solution
Use `contextBridge.exposeInMainWorld()` in preload.js to expose a typed API surface. Main process registers `ipcMain.handle()` handlers.

## Code

### preload.js
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('myApp', {
  // Fire-and-forget (one-way)
  minimize: () => ipcRenderer.send('window-minimize'),
  close: () => ipcRenderer.send('window-close'),

  // Request-response (async, returns Promise)
  getProjects: () => ipcRenderer.invoke('get-projects'),
  createProject: (opts) => ipcRenderer.invoke('create-project', opts),
  launchTool: (tool, path) => ipcRenderer.invoke('launch-tool', tool, path),
  selectFolder: () => ipcRenderer.invoke('select-folder'),
});
```

### main.js
```javascript
const { ipcMain, dialog } = require('electron');

// One-way handlers
ipcMain.on('window-minimize', () => mainWindow?.minimize());
ipcMain.on('window-close', () => mainWindow?.close());

// Async handlers (invoke/handle pattern)
ipcMain.handle('get-projects', async () => {
  const data = JSON.parse(fs.readFileSync(projectsFile, 'utf8'));
  return data.projects || [];
});

ipcMain.handle('select-folder', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory'],
    defaultPath: 'C:\Users\oliver\Desktop'
  });
  return result.canceled ? null : result.filePaths[0];
});
```

### renderer (app.js)
```javascript
// Access the exposed API
const projects = await window.myApp.getProjects();
const folder = await window.myApp.selectFolder();
```

## Key Points
- `ipcRenderer.send()` for fire-and-forget (window controls)
- `ipcRenderer.invoke()` / `ipcMain.handle()` for async request-response
- Always set `contextIsolation: true` and `nodeIntegration: false`
- Preload runs in isolated context — only exposes what you explicitly bridge
- Keep the API surface minimal and typed
