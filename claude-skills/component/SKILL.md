---
name: component
description: >
  Creates a new React component with TypeScript, proper types, and styling.
  Use when asked to create a component, make a new component, build a UI element,
  or add a new section/page/widget.
argument-hint: "[ComponentName]"
---

# Create React Component

Create a new React component named `$0`.

## Before Writing

1. Check the project for existing patterns:
   - Look at other components for import style, naming conventions, file structure
   - Check if the project uses Tailwind, CSS modules, styled-components, or plain CSS
   - Check if components use `"use client"` directive (Next.js App Router)
   - Check if the project uses Framer Motion for animations

2. Determine the correct directory:
   - UI components: `src/components/ui/`
   - Section components: `src/components/sections/`
   - Page components: `src/app/` (Next.js) or `src/pages/`
   - Layout components: `src/components/layout/`

## Component Template

```tsx
"use client"; // Only if using hooks, event handlers, or browser APIs

import { ... } from "react";

interface $0Props {
  // Define all props with proper types
}

export default function $0({ ...props }: $0Props) {
  return (
    // JSX here
  );
}
```

## Rules

- Always use TypeScript with a Props interface
- Always export as default function (not arrow function)
- Match the existing code style in the project exactly
- Use Tailwind classes if the project uses Tailwind
- Add `"use client"` only if the component needs client-side features
- Keep components under 150 lines — split if larger
- Name the file exactly `$0.tsx`
