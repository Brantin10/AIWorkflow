---
title: "Skeleton: Next.js + Three.js Interactive Website"
type: skeleton
stack: "React + Node.js"
category: "frontend"
tags:
  - skill
  - skill/skeleton
  - stack/react
  - stack/nextjs
  - stack/threejs
---
# Skeleton: Next.js + Three.js Interactive Website

## Use Case
Premium interactive websites with 3D scenes, scroll-driven animations, and cinematic motion. Used in [[01-Projects/thesis-web]] and [[01-Projects/website-help-tools]].

## File Structure
```
src/
  app/
    layout.tsx           # Root layout with fonts + metadata
    page.tsx             # Landing page
    globals.css          # Tailwind + custom CSS
  components/
    layout/              # Navigation, Footer
    ui/                  # Buttons, cards, cursor
  sections/              # Page sections (hero, intro, services, work, contact)
  experience/
    canvas/              # SceneCanvas, ExperienceRoot
    scenes/              # Per-section 3D scenes (HeroScene, etc.)
    objects/             # Reusable 3D meshes
    materials/           # Custom Three.js materials
    lights/              # Lighting setups
    postprocessing/      # Bloom, noise, chromatic aberration
  shaders/               # Custom GLSL (vertex, fragment, noise)
  animations/
    timelines/           # GSAP timeline definitions
    scroll/              # Scroll-driven animations
  hooks/                 # useLenis, useScrollProgress, useViewport
  lib/                   # Constants, helpers, asset manifest
```

## Key Patterns
- **Single persistent canvas**: One WebGL context, scenes swap on scroll
- **Scroll-driven**: Lenis smooth scroll + normalized progress (0-1)
- **Separation**: `experience/` for 3D, `sections/` for HTML, `animations/` for motion
- **Performance**: KTX2 textures, hero GLB <3MB, lazy load after hero
- **Accessibility**: Respect `prefers-reduced-motion`, semantic HTML

## Setup Commands
```bash
npx create-next-app@latest --ts --tailwind
npm install three @react-three/fiber @react-three/drei @react-three/postprocessing
npm install gsap framer-motion lenis zustand
```

## Customization Points
- Add scenes in `experience/scenes/`
- Add sections in `sections/`
- Custom shaders in `shaders/`
- GSAP timelines in `animations/timelines/`
