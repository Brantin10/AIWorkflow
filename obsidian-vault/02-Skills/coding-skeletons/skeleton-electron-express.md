---
title: "Skeleton: Electron + Express Dashboard"
type: skeleton
stack: "Node.js"
category: "desktop"
tags:
  - skill
  - skill/skeleton
  - stack/node
  - stack/electron
---
# Skeleton: Electron + Express Dashboard

## Use Case
Desktop dashboard apps with native OS integration + REST API for external tool access. Used in [[01-Projects/orchestrator]].

## File Structure
```
project/
  main.js                # Electron main process + IPC handlers
  preload.js             # contextBridge API exposure
  lib/
    api-server.js        # Express REST API (separate port)
    project.js           # Business logic modules
    launcher.js          # External tool spawning
    status.js            # Health check utilities
  renderer/
    index.html           # Multi-screen UI (show/hide screens)
    app.js               # Frontend logic + command bar
    styles.css            # Dark theme CSS
    particles.js          # Canvas background effects
    web-bridge.js         # REST API shim for browser mode
  data/
    projects.json        # Persistent data (JSON files)
  package.json
```

## Key Files
- `main.js` — All IPC handlers live here. Pattern: `ipcMain.handle('name', async (_, opts) => {...})`
- `preload.js` — contextBridge exposes `window.orchestrator` with all IPC methods
- `lib/api-server.js` — Express app with `express.static()` for web preview mode
- `web-bridge.js` — Maps `window.orchestrator.*` to `fetch()` calls when not in Electron

## Setup Commands
```bash
npm init -y
npm install electron express cors
# In package.json: "main": "main.js", "start": "electron ."
npm start
```

## Key Patterns
- **Dual access**: Electron IPC for GUI, REST API for external tools
- **Screen switching**: `showScreen(id)` hides all `.screen` divs, shows target
- **Command bar**: Text input that parses commands and routes actions
- **Web preview**: `web-bridge.js` shims IPC → REST so the same UI runs in browser

## Customization Points
- Add screens in `index.html` as `<div class="screen">` blocks
- Add IPC handlers in `main.js` + expose in `preload.js`
- Add REST routes in `lib/api-server.js`
- Theme in CSS variables (`:root { --bg, --gold, etc. }`)
