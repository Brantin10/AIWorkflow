---
title: "EADDRINUSE Port Conflict Fix"
created: "2026-03-18"
updated: "2026-03-18"
tags: [playbook, node, express, electron, networking, debugging]
status: active
type: playbook
usefulness: high
read-count: 0
source-project: Orchestrator
---

# EADDRINUSE Port Conflict Fix

## Symptom
```
Error: listen EADDRINUSE: address already in use :::3211
```
Express server fails to start because the port is already taken.

## Common Causes
1. Previous instance of the app still running
2. Another app using the same port
3. Hot-reload restarted but old process didn't die

## Fix

### Find and kill the process (Windows)
```powershell
# Find what's using port 3211
netstat -ano | findstr :3211
# Kill the process by PID
taskkill /PID <pid> /F
```

### Graceful handling in code
```javascript
function startApiServer(port = 3211) {
  const app = createApp();
  const server = app.listen(port, () => {
    console.log(`Server on http://localhost:${port}`);
  });
  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.error(`Port ${port} already in use — API server not started`);
      // App continues without API — IPC still works
    } else {
      console.error(`Server error: ${err.message}`);
    }
  });
  return server;
}
```

### Try/catch at boot (Electron)
```javascript
app.whenReady().then(() => {
  createWindow();
  try { startApiServer(3211); } catch (err) {
    console.error('API server failed:', err.message);
    // App still works — API is optional
  }
});
```

## Key Points
- Handle `EADDRINUSE` gracefully — don't crash the entire app
- Make the API server optional if the app has other access methods (IPC)
- On Windows, `netstat -ano | findstr :<port>` finds the blocking process
- Consider auto-incrementing port if primary is taken
