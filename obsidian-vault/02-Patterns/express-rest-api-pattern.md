---
title: "Express REST API with Electron Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, javascript, express, electron, rest-api]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: Orchestrator
---

# Express REST API with Electron Pattern

## Problem
Electron apps need external access from other tools (CLI scripts, voice assistants). IPC only works within the Electron process.

## Solution
Embed an Express server in the Electron main process. Start it at app boot on a fixed port. External tools make HTTP calls to the same data the Electron UI uses.

## Code

```javascript
const express = require('express');
const cors = require('cors');

function createApp() {
  const app = express();
  app.use(cors({ origin: ['http://localhost:3210', 'http://localhost:3211'] }));
  app.use(express.json({ limit: '1mb' }));

  // Health check
  app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', service: 'orchestrator', version: '1.0.0' });
  });

  // CRUD endpoints
  app.get('/api/projects', (req, res) => { /* ... */ });
  app.get('/api/projects/:name/context', (req, res) => { /* ... */ });
  app.put('/api/projects/:name/phases/:num', (req, res) => { /* ... */ });

  return app;
}

function startApiServer(port = 3211) {
  const app = createApp();
  const server = app.listen(port, () => {
    console.log(`REST server on http://localhost:${port}`);
  });
  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.error(`Port ${port} in use — API not started`);
    }
  });
  return server;
}
```

### Boot from main.js
```javascript
app.whenReady().then(() => {
  createWindow();
  try { startApiServer(3211); } catch (err) {
    console.error('API server failed:', err.message);
  }
});
```

## Key Points
- Start server inside `app.whenReady()` — ensures Electron is initialized
- Handle `EADDRINUSE` gracefully (don't crash the app)
- CORS whitelist only trusted origins
- Same data layer (JSON files, vault) used by both IPC and REST
- `try/catch` around server start — API is optional, app works without it
