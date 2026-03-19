---
title: "Skeleton: Monorepo Real-time Chat App"
type: skeleton
stack: "React + Node.js"
category: "fullstack"
tags:
  - skill
  - skill/skeleton
  - stack/react
  - stack/node
  - stack/socketio
---
# Skeleton: Monorepo Real-time Chat App

## Use Case
Real-time chat/companion apps with shared types, WebSocket communication, and AI integration. Used in [[01-Projects/myhealthai]].

## File Structure
```
project/
  package.json           # Workspaces: ["frontend", "backend", "shared"]
  backend/
    src/
      server.ts          # Express + Socket.io server
      routes/            # REST API routes
      controllers/       # Business logic
      middleware/        # Auth, validation
    prisma/
      schema.prisma      # Database schema
  frontend/
    src/
      pages/             # Route pages
      components/        # UI components
      hooks/             # useSocket, useAuth
  shared/
    types.ts             # Shared TypeScript interfaces
```

## Key Patterns
- **npm workspaces**: Shared types between frontend and backend
- **Socket.io**: Bidirectional real-time messaging
- **Prisma + LibSQL**: Edge-compatible database
- **Zustand**: Lightweight frontend state
- **Concurrently**: Run both servers in dev with one command

## Setup Commands
```bash
# Root package.json with "workspaces": ["frontend", "backend", "shared"]
npm install concurrently -D
# scripts: "dev": "concurrently \"npm run dev -w backend\" \"npm run dev -w frontend\""
npm run dev
```
