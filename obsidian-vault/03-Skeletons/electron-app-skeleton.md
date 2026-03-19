---
title: "Electron App Skeleton"
created: "2026-03-18"
updated: "2026-03-18"
tags: [skeleton, electron, javascript, desktop]
status: active
type: skeleton
usefulness: high
read-count: 0
source-project: Orchestrator
---

# Electron App Skeleton

Frameless Electron app with IPC bridge, Express API server, and custom title bar.

## package.json
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": { "start": "electron ." },
  "devDependencies": { "electron": "^35.0.0" },
  "dependencies": { "express": "^5.2.1", "cors": "^2.8.6" }
}
```

## main.js
```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900, height: 680,
    frame: false,           // Frameless window
    resizable: false,
    backgroundColor: '#0a0e1a',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  mainWindow.loadFile('renderer/index.html');
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => app.quit());

// Window controls
ipcMain.on('window-minimize', () => mainWindow?.minimize());
ipcMain.on('window-close', () => mainWindow?.close());

// Example async handler
ipcMain.handle('get-data', async () => {
  return { items: [] };
});
```

## preload.js
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  minimize: () => ipcRenderer.send('window-minimize'),
  close: () => ipcRenderer.send('window-close'),
  getData: () => ipcRenderer.invoke('get-data'),
});
```

## renderer/index.html
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="title-bar">
    <span>My App</span>
    <div class="controls">
      <button onclick="window.api.minimize()">_</button>
      <button onclick="window.api.close()">X</button>
    </div>
  </div>
  <div id="app"></div>
  <script src="app.js"></script>
</body>
</html>
```

## File Structure
```
my-app/
  main.js
  preload.js
  package.json
  renderer/
    index.html
    app.js
    styles.css
  lib/
    api-server.js    (optional Express API)
  data/
    config.json
```
