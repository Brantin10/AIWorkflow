---
name: 3d-website
description: Build premium interactive 3D websites with cinematic motion, WebGL scenes, smooth scrolling, bold typography, and shader effects. Use when asked to create a 3D website, interactive landing page, WebGL experience, agency-style site, immersive web experience, or anything involving Three.js / React Three Fiber / GSAP animations.
---

This skill scaffolds and builds premium interactive 3D websites using a battle-tested template. It produces production-ready code with a loading overlay, adaptive GPU quality, smooth scrolling, 3D scenes, and accessibility baked in.

The user provides a website concept, brand, or brief. You scaffold the full foundation from the code templates below, then build the custom 3D scene and content sections on top.

## Tech Stack (Non-Negotiable)

```json
{
  "dependencies": {
    "@gsap/react": "^2.1.2",
    "@react-three/drei": "^10.7.7",
    "@react-three/fiber": "^9.5.0",
    "@react-three/postprocessing": "^3.0.4",
    "clsx": "^2.1.1",
    "framer-motion": "^12.35.2",
    "gsap": "^3.14.2",
    "lenis": "^1.3.18",
    "next": "16.1.6",
    "react": "19.2.3",
    "react-dom": "19.2.3",
    "three": "^0.183.2",
    "zustand": "^5.0.11"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "@types/three": "^0.183.1",
    "eslint": "^9",
    "eslint-config-next": "16.1.6",
    "tailwindcss": "^4",
    "typescript": "^5"
  }
}
```

## Architecture — Separation of Concerns

```
src/
├── app/               # Next.js App Router (layout.tsx, page.tsx, globals.css)
├── components/        # DOM components
│   ├── layout/        # Navigation, Footer
│   └── ui/            # CustomCursor, AudioControls, etc.
├── experience/        # ALL 3D/WebGL code
│   ├── SceneCanvas.tsx       # Canvas + LoadingOverlay (use template below)
│   ├── HeroScene.tsx         # Main 3D scene (custom per project)
│   ├── PostProcessing.tsx    # Bloom, glow (optional)
│   └── ChromaticAberration.tsx
├── hooks/             # Custom hooks (use templates below)
├── lib/               # Utilities (qualityPresets, heartbeat, etc.)
├── sections/          # HTML content sections (Hero, About, Work, Contact)
├── store/             # Zustand state (use template below)
├── shaders/           # GLSL files (optional, can inline)
└── animations/        # GSAP timelines (optional, can inline)
public/
├── fonts/
├── models/
└── textures/
```

### Canvas Strategy
- ONE persistent `<SceneCanvas>` fixed behind all content
- HTML sections overlay above via `.content-layer` (z-index: 1)
- Single camera with scroll-based + mouse parallax interpolation
- `<Preload all />` triggers loading overlay progress

### Animation Strategy
- GSAP for deterministic timelines and scroll-driven transitions
- Framer Motion ONLY for lightweight DOM interactions (hover, reveal)
- `useAnimationFrame` hook wraps `useFrame` — auto-skips when `prefers-reduced-motion` is active
- Heartbeat utility for synchronized organic pulsing across 3D elements

---

## CODE TEMPLATES

Generate these files exactly as shown, replacing `{{PLACEHOLDERS}}` with project-specific values. These are proven, production-tested patterns.

---

### `src/app/globals.css`

Adapt colors to the user's brand. Keep the canvas/content layer strategy and Lenis rules intact.

```css
@import "tailwindcss";

@theme inline {
  --color-background: {{BACKGROUND_COLOR}};    /* e.g. #0A0A0A or #E8F0FA */
  --color-surface: {{SURFACE_COLOR}};          /* slightly offset from bg */
  --color-primary: {{PRIMARY_TEXT_COLOR}};      /* main text */
  --color-secondary: {{SECONDARY_TEXT_COLOR}};  /* muted text */
  --color-accent: {{ACCENT_COLOR}};            /* brand highlight */
  --color-accent-soft: {{ACCENT_SOFT}};        /* softer accent variant */
  --color-accent-glow: {{ACCENT_GLOW_RGBA}};   /* e.g. rgba(255,154,46,0.25) */
  --font-sans: var(--font-{{FONT_VARIABLE}});
  --font-mono: var(--font-geist-mono);
}

@layer base {
  * { margin: 0; padding: 0; box-sizing: border-box; }
}

html { scroll-behavior: auto; }

body {
  background: var(--color-background);
  color: var(--color-primary);
  font-family: var(--font-sans), system-ui, -apple-system, sans-serif;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Lenis smooth scroll — required */
html.lenis, html.lenis body { height: auto; }
.lenis.lenis-smooth { scroll-behavior: auto !important; }
.lenis.lenis-smooth [data-lenis-prevent] { overscroll-behavior: contain; }
.lenis.lenis-stopped { overflow: hidden; }

/* Canvas layer — fixed behind content */
.canvas-container {
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 0; pointer-events: none;
}
.canvas-container canvas { pointer-events: auto; }

/* Content layer — scrollable above canvas */
.content-layer { position: relative; z-index: 1; }

/* Typography scale */
.text-display { font-size: clamp(3rem, 8vw, 7rem); line-height: 0.95; letter-spacing: -0.03em; font-weight: 700; }
.text-h1 { font-size: clamp(2.5rem, 6vw, 5rem); line-height: 1; letter-spacing: -0.02em; font-weight: 700; }
.text-h2 { font-size: clamp(1.75rem, 4vw, 3rem); line-height: 1.1; letter-spacing: -0.01em; font-weight: 600; }
.text-body { font-size: clamp(1rem, 1.2vw, 1.125rem); line-height: 1.7; }

::selection { background: var(--color-accent-glow); color: var(--color-primary); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--color-surface); }
::-webkit-scrollbar-thumb { background: var(--color-secondary); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--color-accent); }

/* Reduced motion — accessibility critical */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

### `src/app/layout.tsx`

```tsx
import type { Metadata } from "next";
import { {{FONT_IMPORT}} } from "next/font/google";
import "./globals.css";

const font = {{FONT_IMPORT}}({
  variable: "--font-{{FONT_VARIABLE}}",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "{{SITE_TITLE}}",
  description: "{{SITE_DESCRIPTION}}",
  openGraph: {
    title: "{{OG_TITLE}}",
    description: "{{OG_DESCRIPTION}}",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${font.variable} antialiased`}>{children}</body>
    </html>
  );
}
```

---

### `src/app/page.tsx` — Main Entry Point

Boot sequence: initialize all system hooks, render canvas + content layers.

```tsx
"use client";

import { SceneCanvas } from "@/experience/SceneCanvas";
import { Navigation } from "@/components/layout/Navigation";
import { Footer } from "@/components/layout/Footer";
import { CustomCursor } from "@/components/ui/CustomCursor";
import { useScrollProgress } from "@/hooks/useScrollProgress";
import { useViewport } from "@/hooks/useViewport";
import { useLenisScroll } from "@/hooks/useLenis";
import { useAdaptiveQuality } from "@/hooks/useAdaptiveQuality";
// Import your sections here

export default function Home() {
  useScrollProgress();
  useViewport();
  useLenisScroll();
  useAdaptiveQuality();

  return (
    <>
      <SceneCanvas />
      <Navigation />
      <main className="content-layer">
        {/* Your sections here */}
      </main>
      <Footer />
      <CustomCursor />
    </>
  );
}
```

---

### `src/store/useAppStore.ts` — Global State

Core state that drives quality, loading, scroll, and accessibility across all components.

```tsx
import { create } from "zustand";
import type { QualityLevel } from "@/lib/qualityPresets";

interface AppState {
  isLoaded: boolean;
  scrollProgress: number;
  isMobile: boolean;
  reducedMotion: boolean;
  qualityLevel: QualityLevel;
  hoveredRegion: string | null;

  setLoaded: (loaded: boolean) => void;
  setScrollProgress: (progress: number) => void;
  setIsMobile: (mobile: boolean) => void;
  setReducedMotion: (reduced: boolean) => void;
  setQualityLevel: (level: QualityLevel) => void;
  setHoveredRegion: (id: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isLoaded: false,
  scrollProgress: 0,
  isMobile: false,
  reducedMotion: false,
  qualityLevel: "medium",
  hoveredRegion: null,

  setLoaded: (loaded) => set({ isLoaded: loaded }),
  setScrollProgress: (progress) => set({ scrollProgress: progress }),
  setIsMobile: (mobile) => set({ isMobile: mobile }),
  setReducedMotion: (reduced) => set({ reducedMotion: reduced }),
  setQualityLevel: (level) => set({ qualityLevel: level }),
  setHoveredRegion: (id) => set({ hoveredRegion: id }),
}));
```

Extend with project-specific state (audio, TTS, interactive regions, etc.) as needed.

---

### `src/lib/qualityPresets.ts` — Adaptive GPU Quality

```tsx
export type QualityLevel = "low" | "medium" | "high";

export interface QualitySettings {
  particleCount: number;
  dpr: [number, number];
  enablePostProcessing: boolean;
  enableChromaticAberration: boolean;
  chromaticStrength: number;
  shaderDetail: "simple" | "full";
}

export const QUALITY_PRESETS: Record<QualityLevel, QualitySettings> = {
  low: {
    particleCount: 200,
    dpr: [1, 1],
    enablePostProcessing: false,
    enableChromaticAberration: false,
    chromaticStrength: 0,
    shaderDetail: "simple",
  },
  medium: {
    particleCount: 600,
    dpr: [1, 1.5],
    enablePostProcessing: true,
    enableChromaticAberration: true,
    chromaticStrength: 0.002,
    shaderDetail: "full",
  },
  high: {
    particleCount: 1500,
    dpr: [1, 2],
    enablePostProcessing: true,
    enableChromaticAberration: true,
    chromaticStrength: 0.004,
    shaderDetail: "full",
  },
};
```

Add project-specific quality fields (sparkleCount, backgroundParticles, etc.) as needed.

---

### `src/lib/heartbeat.ts` — Synchronized Pulse

Shared organic pulse used across all 3D elements. Period ~2.513s, shaped for sharp spikes.

```tsx
export function getHeartbeat(t: number, delay = 0): number {
  return Math.pow(Math.max(0, Math.sin((t - delay) * 2.5) * 0.5 + 0.5), 4);
}

export const HEARTBEAT_PERIOD = (2 * Math.PI) / 2.5;
```

Use staggered `delay` values (0.06, 0.12, 0.18...) for organic wave effects across multiple elements.

---

### `src/experience/SceneCanvas.tsx` — Canvas + Loading Overlay

The most critical file. Includes: background shader, mouse parallax, loading overlay with real progress, suspense fallback.

```tsx
"use client";

import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { Suspense, useEffect, useRef, useState } from "react";
import { Preload, useProgress } from "@react-three/drei";
import * as THREE from "three";
import { useAppStore } from "@/store/useAppStore";
import { useAnimationFrame } from "@/hooks/useAnimationFrame";
import { QUALITY_PRESETS } from "@/lib/qualityPresets";
// Import your HeroScene and PostProcessing here

// ─── Background Shader ───────────────────────────────────────────────────────
// Customize colors and effects per project. This example: radial gradient + stars + dot grid.

const bgVertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const bgFragmentShader = `
  precision highp float;
  varying vec2 vUv;
  uniform float uTime;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
  }

  void main() {
    vec2 center = vec2(0.5);
    float dist = distance(vUv, center);

    // Radial gradient — customize these two colors per project
    vec3 colorCenter = vec3({{BG_CENTER_RGB}});
    vec3 colorEdge = vec3({{BG_EDGE_RGB}});
    vec3 col = mix(colorCenter, colorEdge, smoothstep(0.0, 0.70, dist));

    // Vignette
    col *= 1.0 - smoothstep(0.5, 0.85, dist) * 0.08;

    // Star field
    vec2 starUv = vUv * 120.0;
    vec2 starCell = floor(starUv);
    float starHash = hash(starCell);
    if (starHash > 0.92) {
      vec2 starPos = vec2(hash(starCell + 0.5), hash(starCell + 1.5));
      float starDist = length(fract(starUv) - starPos);
      float star = 1.0 - smoothstep(0.0, 0.02 + starHash * 0.03, starDist);
      float twinkle = sin(uTime * (1.0 + starHash * 2.0) + starHash * 6.2832) * 0.5 + 0.5;
      col += vec3(0.95, 0.97, 1.0) * star * (0.3 + twinkle * 0.5) * 0.6;
    }

    // Dot grid (optional HUD feel)
    vec2 gridUv = vUv * 50.0;
    float dot = 1.0 - smoothstep(0.0, 0.12, length(fract(gridUv) - 0.5));
    float pulse = sin(uTime * 0.6 + floor(gridUv.x) * 7.3 + floor(gridUv.y) * 13.7) * 0.5 + 0.5;
    col += vec3(0.7, 0.82, 1.0) * dot * 0.03 * (0.4 + pulse * 0.6);

    // Breathing
    col += 0.005 * sin(uTime * 0.4 + dist * 2.5);

    gl_FragColor = vec4(col, 1.0);
  }
`;

function GradientBackground() {
  const matRef = useRef<THREE.ShaderMaterial>(null);
  useAnimationFrame((_, delta) => {
    if (matRef.current) matRef.current.uniforms.uTime.value += delta;
  });
  return (
    <mesh position={[0, 0, -20]} renderOrder={-1}>
      <planeGeometry args={[60, 40]} />
      <shaderMaterial
        ref={matRef}
        vertexShader={bgVertexShader}
        fragmentShader={bgFragmentShader}
        uniforms={{ uTime: { value: 0 } }}
        depthWrite={false}
        depthTest={false}
      />
    </mesh>
  );
}

function SceneSetup() {
  const { gl } = useThree();
  useEffect(() => { gl.setClearColor(new THREE.Color("{{CLEAR_COLOR}}"), 1); }, [gl]);
  return null;
}

// ─── Mouse Parallax ──────────────────────────────────────────────────────────

function MouseParallax() {
  const { camera } = useThree();
  const reducedMotion = useAppStore((s) => s.reducedMotion);
  const mouse = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      mouse.current.x = (e.clientX / window.innerWidth - 0.5) * 2;
      mouse.current.y = (e.clientY / window.innerHeight - 0.5) * 2;
    };
    window.addEventListener("mousemove", handler);
    return () => window.removeEventListener("mousemove", handler);
  }, []);

  useFrame(() => {
    if (reducedMotion) return;
    camera.position.x = THREE.MathUtils.lerp(camera.position.x, mouse.current.x * 0.5, 0.05);
    camera.position.y = THREE.MathUtils.lerp(camera.position.y, -mouse.current.y * 0.3, 0.05);
  });

  return null;
}

// ─── Loading Overlay ─────────────────────────────────────────────────────────
// Real progress tracking via drei's useProgress. Handles procedural scenes (no assets).

function LoadingOverlay() {
  const { progress, active, loaded, total } = useProgress();
  const setLoaded = useAppStore((s) => s.setLoaded);
  const [visible, setVisible] = useState(true);
  const [fading, setFading] = useState(false);

  useEffect(() => {
    // Procedural scene (no assets queued) — auto-dismiss after delay
    if (!active && total === 0) {
      const timer = setTimeout(() => {
        setFading(true);
        setTimeout(() => { setVisible(false); setLoaded(true); }, 700);
      }, 600);
      return () => clearTimeout(timer);
    }

    // Normal: assets finished loading
    if (!active && progress === 100) {
      const timer = setTimeout(() => {
        setFading(true);
        setTimeout(() => { setVisible(false); setLoaded(true); }, 700);
      }, 400);
      return () => clearTimeout(timer);
    }
  }, [active, progress, total, setLoaded]);

  if (!visible) return null;
  const displayProgress = fading ? 100 : Math.round(progress);

  return (
    <div className={`fixed inset-0 z-50 flex items-center justify-center bg-background transition-opacity duration-700 ${fading ? "opacity-0" : "opacity-100"}`}>
      <div className="flex flex-col items-center gap-4">
        <div className="h-1 w-48 overflow-hidden rounded-full bg-accent/10">
          <div className="h-full rounded-full bg-accent transition-all duration-300 ease-out" style={{ width: `${displayProgress}%` }} />
        </div>
        <p className="font-mono text-sm tabular-nums text-secondary">{displayProgress}%</p>
        <p className="text-xs text-secondary/60">Loading experience...</p>
      </div>
    </div>
  );
}

function SuspenseFallback() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background">
      <div className="flex flex-col items-center gap-4">
        <div className="h-1 w-48 overflow-hidden rounded-full bg-accent/10">
          <div className="h-full w-1/3 animate-pulse rounded-full bg-accent" />
        </div>
        <p className="text-sm text-secondary">Loading experience...</p>
      </div>
    </div>
  );
}

// ─── Canvas Export ────────────────────────────────────────────────────────────

export function SceneCanvas() {
  const isMobile = useAppStore((s) => s.isMobile);
  const qualityLevel = useAppStore((s) => s.qualityLevel);
  const quality = QUALITY_PRESETS[qualityLevel];

  return (
    <div className="canvas-container">
      <Suspense fallback={<SuspenseFallback />}>
        <Canvas
          camera={{ position: [0, 0, 8], fov: 50 }}
          dpr={quality.dpr}
          gl={{ antialias: true, alpha: false, powerPreference: "high-performance" }}
          style={{ background: "{{CANVAS_BG_HEX}}" }}
        >
          <SceneSetup />
          <MouseParallax />
          <GradientBackground />
          {/* <HeroScene /> — your custom 3D scene */}
          {/* {!isMobile && <PostProcessing />} */}
          <Preload all />
        </Canvas>
      </Suspense>
      <LoadingOverlay />
    </div>
  );
}
```

---

### `src/hooks/useAnimationFrame.ts` — Reduced-Motion Aware useFrame

```tsx
"use client";

import { useFrame, type RootState } from "@react-three/fiber";
import { useAppStore } from "@/store/useAppStore";

export function useAnimationFrame(
  callback: (state: RootState, delta: number) => void,
  priority?: number
) {
  const reducedMotion = useAppStore((s) => s.reducedMotion);
  useFrame((state, delta) => {
    if (reducedMotion) return;
    callback(state, delta);
  }, priority);
}
```

---

### `src/hooks/useViewport.ts` — Mobile + Reduced Motion Detection

```tsx
"use client";

import { useEffect } from "react";
import { useAppStore } from "@/store/useAppStore";

export function useViewport() {
  const setIsMobile = useAppStore((s) => s.setIsMobile);
  const setReducedMotion = useAppStore((s) => s.setReducedMotion);

  useEffect(() => {
    function checkMobile() { setIsMobile(window.innerWidth < 768); }

    const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(motionQuery.matches);

    function handleMotionChange(e: MediaQueryListEvent) { setReducedMotion(e.matches); }

    checkMobile();
    window.addEventListener("resize", checkMobile);
    motionQuery.addEventListener("change", handleMotionChange);

    return () => {
      window.removeEventListener("resize", checkMobile);
      motionQuery.removeEventListener("change", handleMotionChange);
    };
  }, [setIsMobile, setReducedMotion]);
}
```

---

### `src/hooks/useAdaptiveQuality.ts` — GPU Tier Detection

```tsx
"use client";

import { useEffect } from "react";
import { useAppStore } from "@/store/useAppStore";
import type { QualityLevel } from "@/lib/qualityPresets";

export function useAdaptiveQuality() {
  const isMobile = useAppStore((s) => s.isMobile);
  const setQualityLevel = useAppStore((s) => s.setQualityLevel);

  useEffect(() => {
    async function detect() {
      try {
        const { getGPUTier } = await import("detect-gpu");
        const gpuTier = await getGPUTier();
        let level: QualityLevel;
        if (isMobile || gpuTier.tier <= 1) level = "low";
        else if (gpuTier.tier === 2) level = "medium";
        else level = "high";
        setQualityLevel(level);
        console.log(`[AdaptiveQuality] GPU tier: ${gpuTier.tier} (${gpuTier.gpu}), quality: ${level}`);
      } catch {
        setQualityLevel("medium");
        console.warn("[AdaptiveQuality] GPU detection failed, defaulting to medium");
      }
    }
    detect();
  }, [isMobile, setQualityLevel]);
}
```

---

### `src/hooks/useScrollProgress.ts` — Normalized Scroll 0→1

```tsx
"use client";

import { useEffect } from "react";
import { useAppStore } from "@/store/useAppStore";

export function useScrollProgress() {
  const setScrollProgress = useAppStore((s) => s.setScrollProgress);

  useEffect(() => {
    function handleScroll() {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? window.scrollY / docHeight : 0;
      setScrollProgress(Math.min(Math.max(progress, 0), 1));
    }
    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, [setScrollProgress]);
}
```

---

### `src/hooks/useLenis.ts` — Smooth Scroll

```tsx
"use client";

import { useEffect, useRef } from "react";
import Lenis from "lenis";
import { useAppStore } from "@/store/useAppStore";

export function useLenisScroll() {
  const lenisRef = useRef<Lenis | null>(null);
  const reducedMotion = useAppStore((s) => s.reducedMotion);

  useEffect(() => {
    if (reducedMotion) return;
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      touchMultiplier: 2,
    });
    lenisRef.current = lenis;
    function raf(time: number) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    return () => { lenis.destroy(); lenisRef.current = null; };
  }, [reducedMotion]);

  return lenisRef;
}
```

---

### `src/components/ui/CustomCursor.tsx` — DOM Cursor with Trail

Optional but adds premium feel. Zero GPU overhead — pure DOM/CSS.

```tsx
"use client";

import { useEffect, useRef, useCallback } from "react";
import { useAppStore } from "@/store/useAppStore";

const TRAIL_COUNT = 5;
const LERP_SPEED = 0.15;
const TRAIL_LERP = 0.25;

export function CustomCursor() {
  const isMobile = useAppStore((s) => s.isMobile);
  const reducedMotion = useAppStore((s) => s.reducedMotion);
  const hoveredRegion = useAppStore((s) => s.hoveredRegion);

  const mainRef = useRef<HTMLDivElement>(null);
  const trailRefs = useRef<(HTMLDivElement | null)[]>([]);
  const mouse = useRef({ x: -100, y: -100 });
  const pos = useRef({ x: -100, y: -100 });
  const trailPos = useRef(Array.from({ length: TRAIL_COUNT }, () => ({ x: -100, y: -100 })));
  const rafId = useRef<number>(0);

  const setTrailRef = useCallback((index: number) => (el: HTMLDivElement | null) => {
    trailRefs.current[index] = el;
  }, []);

  useEffect(() => {
    if (isMobile || reducedMotion) return;
    const handleMouse = (e: MouseEvent) => { mouse.current.x = e.clientX; mouse.current.y = e.clientY; };
    window.addEventListener("mousemove", handleMouse);

    const animate = () => {
      pos.current.x += (mouse.current.x - pos.current.x) * LERP_SPEED;
      pos.current.y += (mouse.current.y - pos.current.y) * LERP_SPEED;
      if (mainRef.current) {
        mainRef.current.style.transform = `translate(${pos.current.x}px, ${pos.current.y}px) translate(-50%, -50%)`;
      }
      for (let i = 0; i < TRAIL_COUNT; i++) {
        const target = i === 0 ? pos.current : trailPos.current[i - 1];
        const trail = trailPos.current[i];
        trail.x += (target.x - trail.x) * TRAIL_LERP * (1 - i * 0.04);
        trail.y += (target.y - trail.y) * TRAIL_LERP * (1 - i * 0.04);
        const el = trailRefs.current[i];
        if (el) el.style.transform = `translate(${trail.x}px, ${trail.y}px) translate(-50%, -50%)`;
      }
      rafId.current = requestAnimationFrame(animate);
    };
    rafId.current = requestAnimationFrame(animate);
    return () => { window.removeEventListener("mousemove", handleMouse); cancelAnimationFrame(rafId.current); };
  }, [isMobile, reducedMotion]);

  if (isMobile || reducedMotion) return null;
  const isHovering = hoveredRegion !== null;
  const accentColor = "{{CURSOR_COLOR}}"; // e.g. "#d07018"

  return (
    <>
      <style>{`@media (pointer: fine) { body { cursor: none !important; } a, button, [role="button"] { cursor: none !important; } }`}</style>
      {Array.from({ length: TRAIL_COUNT }, (_, i) => (
        <div key={i} ref={setTrailRef(i)} style={{
          position: "fixed", top: 0, left: 0,
          width: `${Math.max(3, 6 - i)}px`, height: `${Math.max(3, 6 - i)}px`,
          borderRadius: "50%", backgroundColor: accentColor,
          opacity: 0.4 - i * 0.07, pointerEvents: "none", zIndex: 9998,
          willChange: "transform", transition: "width 0.3s, height 0.3s",
        }} />
      ))}
      <div ref={mainRef} style={{
        position: "fixed", top: 0, left: 0,
        width: isHovering ? "24px" : "8px", height: isHovering ? "24px" : "8px",
        borderRadius: "50%",
        backgroundColor: isHovering ? `${accentColor}4D` : accentColor,
        border: isHovering ? `2px solid ${accentColor}` : "none",
        boxShadow: isHovering ? `0 0 20px ${accentColor}80, 0 0 40px ${accentColor}33` : "none",
        pointerEvents: "none", zIndex: 9999, willChange: "transform",
        transition: "width 0.3s, height 0.3s, background-color 0.3s, box-shadow 0.3s, border 0.3s",
      }} />
    </>
  );
}
```

---

## Scaffolding Checklist

When the user invokes this skill, generate files in this order:

1. `package.json` — use dependencies from tech stack above
2. `src/app/globals.css` — from template, replace color placeholders
3. `src/app/layout.tsx` — from template, replace font + metadata
4. `src/store/useAppStore.ts` — from template
5. `src/lib/qualityPresets.ts` — from template
6. `src/lib/heartbeat.ts` — from template
7. `src/hooks/useAnimationFrame.ts` — exact copy
8. `src/hooks/useViewport.ts` — exact copy
9. `src/hooks/useAdaptiveQuality.ts` — exact copy
10. `src/hooks/useScrollProgress.ts` — exact copy
11. `src/hooks/useLenis.ts` — exact copy
12. `src/experience/SceneCanvas.tsx` — from template, customize background shader colors
13. `src/components/ui/CustomCursor.tsx` — from template, set accent color
14. `src/app/page.tsx` — from template, add project sections
15. `src/components/layout/Navigation.tsx` — custom per project
16. `src/components/layout/Footer.tsx` — custom per project
17. `src/sections/Hero.tsx` — custom per project
18. `src/experience/HeroScene.tsx` — custom 3D scene per project

Then `npm install` and start building the custom 3D scene + content sections.

## Design System Defaults

If the user doesn't provide brand colors, use:

### Dark Theme (Default)
```
background: #0A0A0A | surface: #121212 | primary: #FFFFFF
secondary: #A1A1AA | accent: #7C5CFF | accent-glow: rgba(124,92,255,0.25)
```

### Light Theme (Alternative)
```
background: #E8F0FA | surface: #E0EAF4 | primary: #1a1408
secondary: #7a6548 | accent: #ff9a2e | accent-glow: rgba(255,154,46,0.25)
```

Override with user's brand colors when provided.

### Typography
- **Fonts**: Space Grotesk (default), Satoshi, Neue Montreal, or user's brand font
- Oversized display text with generous whitespace
- Sharp contrast between stillness and motion

## Visual Direction

- **Minimal but dramatic** — premium agency/studio feel
- **Full viewport hero** with immediate 3D visual impact
- **Strong vertical rhythm** — avoid cluttered UI
- **3D motion supports content**, never distracts
- **Editorial layout** with cinematic transitions

## Performance Budget

- Hero GLB < 3 MB, total initial payload < 5 MB
- Compress textures (KTX2/WebP)
- Clamp DPR on low-powered devices via qualityPresets
- Disable post-processing on mobile
- Pause expensive updates when tab is inactive
- Use `<Preload all />` for proper loading overlay progress

## Accessibility (Non-Negotiable)

- Semantic HTML for all content sections
- Keyboard-accessible navigation
- `useAnimationFrame` auto-respects `prefers-reduced-motion`
- `useLenisScroll` auto-disables on reduced motion
- `CustomCursor` auto-hides on mobile and reduced motion
- Readable text contrast + proper heading structure

## What To Ask The User

Before building, gather:
- **Brand**: name, tagline, colors, fonts
- **Copy**: hero headline, section text, CTA
- **3D Direction**: what object/scene for the hero (geometric, organic, product, abstract)
- **Mood**: dark/light, minimal/maximal, playful/serious

If not provided, use compelling placeholder content with the dark theme defaults.
