---
name: jarvis-electron
description: Build Jarvis-style Electron desktop apps with holographic WebGL orb, frameless transparent window, system tray, global hotkeys, and state-driven animations. Use when asked to create a desktop app, Electron app, holographic UI, orb visualization, AI assistant UI, or transparent overlay app.
---

This skill scaffolds Electron desktop applications with a cinematic holographic UI inspired by Iron Man's JARVIS. It produces a frameless, transparent, always-on-top window with a full-screen WebGL holographic orb that responds to application state (idle → listening → thinking → speaking) via smooth color transitions, voice pulse rings, and structural animations.

The user provides an app concept. You scaffold the full Electron + React + Three.js foundation from the templates below, then customize the 3D scene, IPC logic, and backend integration.

## Tech Stack (Non-Negotiable)

```json
{
  "dependencies": {
    "@react-three/fiber": "^9.5.0",
    "@react-three/drei": "^10.7.7",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "three": "^0.183.2",
    "zustand": "^5.0.11",
    "clsx": "^2.1.1"
  },
  "devDependencies": {
    "electron": "^34.0.0",
    "electron-builder": "^25.0.0",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "@types/three": "^0.183.1",
    "typescript": "^5",
    "vite": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "vite-plugin-electron": "^0.28.0",
    "vite-plugin-electron-renderer": "^0.14.0",
    "tailwindcss": "^4",
    "@tailwindcss/vite": "^4"
  }
}
```

## Architecture

```
├── electron/
│   ├── main.ts              # Main process (window, tray, shortcuts, IPC)
│   ├── preload.ts           # IPC bridge (contextBridge)
│   └── tsconfig.json
├── src/
│   ├── App.tsx              # Root renderer component
│   ├── main.tsx             # React entry point
│   ├── index.html           # HTML shell
│   ├── globals.css          # Transparent background, fonts, scrollbar
│   ├── components/
│   │   ├── HologramOrb.tsx  # Three.js holographic orb (GLSL shader)
│   │   ├── TitleBar.tsx     # Frameless window drag handle + controls
│   │   └── StatusBar.tsx    # Bottom status text + mic button
│   ├── store/
│   │   └── useAppStore.ts   # Zustand state (state machine, colors)
│   └── lib/
│       └── stateConfig.ts   # State colors + animation configs
├── vite.config.ts
├── package.json
└── electron-builder.yml
```

### Key Patterns
- **ONE WebGL canvas** fills the entire transparent window — the hologram IS the app
- **Frameless transparent window** — Electron `transparent: true` + no frame
- **State machine** drives everything: `idle → listening → thinking → speaking`
- **Smooth lerp transitions** between states (colors, intensity, energy, speed)
- **System tray** with right-click menu (Show/Hide, Quit)
- **Global shortcut** (Ctrl+Alt+J or customizable) for activation
- **IPC bridge** for renderer ↔ main process communication
- **Additive blending** — bright hologram glows on transparent/dark background

---

## CODE TEMPLATES

Replace `{{PLACEHOLDERS}}` with project-specific values.

---

### `electron/main.ts` — Main Process

Frameless transparent window + system tray + global shortcuts + IPC.

```typescript
import { app, BrowserWindow, Tray, Menu, globalShortcut, ipcMain, nativeImage } from "electron";
import path from "path";

let win: BrowserWindow | null = null;
let tray: Tray | null = null;

// ─── Window ──────────────────────────────────────────────────────────────────

function createWindow() {
  win = new BrowserWindow({
    width: {{WINDOW_WIDTH}},   // e.g. 800
    height: {{WINDOW_HEIGHT}}, // e.g. 800
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    hasShadow: false,
    skipTaskbar: true,
    backgroundColor: "#00000000",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  // Center on screen
  win.center();

  // Vite dev server or production build
  if (process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL);
  } else {
    win.loadFile(path.join(__dirname, "../dist/index.html"));
  }

  // Prevent close — hide to tray instead
  win.on("close", (e) => {
    if (!app.isQuitting) {
      e.preventDefault();
      win?.hide();
    }
  });

  win.on("closed", () => { win = null; });
}

// ─── System Tray ─────────────────────────────────────────────────────────────

function createTray() {
  // Create a simple tray icon (cyan dot on dark background)
  const icon = nativeImage.createEmpty();
  // In production, use: nativeImage.createFromPath(path.join(__dirname, "icon.png"))
  tray = new Tray(icon);
  tray.setToolTip("{{APP_NAME}} — Online");

  const contextMenu = Menu.buildFromTemplate([
    {
      label: "Show / Hide",
      click: () => {
        if (win?.isVisible()) {
          win.hide();
        } else {
          win?.show();
          win?.focus();
        }
      },
    },
    { type: "separator" },
    {
      label: "Quit",
      click: () => {
        app.isQuitting = true;
        app.quit();
      },
    },
  ]);

  tray.setContextMenu(contextMenu);
  tray.on("double-click", () => {
    if (win?.isVisible()) {
      win.hide();
    } else {
      win?.show();
      win?.focus();
    }
  });
}

// ─── Global Shortcut ─────────────────────────────────────────────────────────

function registerShortcuts() {
  globalShortcut.register("{{GLOBAL_SHORTCUT}}", () => {
    // e.g. "CommandOrControl+Alt+J"
    if (win?.isVisible()) {
      win.hide();
    } else {
      win?.show();
      win?.focus();
    }
    // Notify renderer
    win?.webContents.send("shortcut-activated");
  });
}

// ─── IPC Handlers ────────────────────────────────────────────────────────────

function setupIPC() {
  ipcMain.handle("get-app-state", () => {
    return { visible: win?.isVisible() ?? false };
  });

  ipcMain.on("set-state", (_event, state: string) => {
    // Forward state changes if needed
    console.log(`[Main] State: ${state}`);
  });

  ipcMain.on("set-click-through", (_event, enabled: boolean) => {
    if (win) {
      win.setIgnoreMouseEvents(enabled, { forward: true });
      console.log(`[Main] Click-through: ${enabled}`);
    }
  });

  // Window controls from frameless title bar
  ipcMain.on("window-minimize", () => win?.minimize());
  ipcMain.on("window-close", () => win?.hide());
}

// ─── App Lifecycle ───────────────────────────────────────────────────────────

app.whenReady().then(() => {
  createWindow();
  createTray();
  registerShortcuts();
  setupIPC();
});

app.on("will-quit", () => {
  globalShortcut.unregisterAll();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

// Extend app type for isQuitting flag
declare module "electron" {
  interface App {
    isQuitting?: boolean;
  }
}
```

---

### `electron/preload.ts` — IPC Bridge

```typescript
import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronAPI", {
  // Main → Renderer
  onShortcutActivated: (callback: () => void) => {
    ipcRenderer.on("shortcut-activated", callback);
  },

  // Renderer → Main
  setState: (state: string) => ipcRenderer.send("set-state", state),
  setClickThrough: (enabled: boolean) => ipcRenderer.send("set-click-through", enabled),
  windowMinimize: () => ipcRenderer.send("window-minimize"),
  windowClose: () => ipcRenderer.send("window-close"),
  getAppState: () => ipcRenderer.invoke("get-app-state"),
});
```

Add type declarations in `src/types/electron.d.ts`:

```typescript
export interface ElectronAPI {
  onShortcutActivated: (callback: () => void) => void;
  setState: (state: string) => void;
  setClickThrough: (enabled: boolean) => void;
  windowMinimize: () => void;
  windowClose: () => void;
  getAppState: () => Promise<{ visible: boolean }>;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
```

---

### `src/globals.css` — Transparent Background

```css
@import "tailwindcss";

@theme inline {
  --color-background: transparent;
  --color-surface: rgba(10, 22, 40, 0.6);
  --color-primary: rgba(255, 220, 140, 0.95);
  --color-secondary: rgba(255, 200, 120, 0.6);
  --color-accent: {{ACCENT_COLOR}};       /* e.g. #ff9a2e (Jarvis orange) or #00d4ff (cyan) */
  --color-accent-glow: {{ACCENT_GLOW}};   /* e.g. rgba(255,154,46,0.4) */
  --font-mono: "Consolas", "Courier New", monospace;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, #root {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: transparent;
  color: var(--color-primary);
  font-family: var(--font-mono);
  -webkit-font-smoothing: antialiased;
  user-select: none;
}

/* Frameless window drag region */
.drag-region {
  -webkit-app-region: drag;
}
.no-drag {
  -webkit-app-region: no-drag;
}

/* Scrollbar (for any scrollable panels) */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--color-secondary); border-radius: 2px; }
```

---

### `src/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{APP_NAME}}</title>
    <style>
      /* Ensure transparent before React mounts */
      html, body { background: transparent !important; margin: 0; }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

### `src/main.tsx`

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./globals.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

### `src/lib/stateConfig.ts` — State Machine Colors & Animation Configs

Ported directly from JARVIS Python brain_renderer.py. All orange tones differentiated by warmth/brightness.

```typescript
export type AppState = "idle" | "listening" | "thinking" | "speaking";

export interface StateColors {
  base: [number, number, number];
  hi: [number, number, number];
  hot: [number, number, number];
}

export interface StateConfig {
  intensity: number;
  speed: number;
  energy: number;
  speak: number; // 0.0 = silent, 1.0 = speaking (drives pulse rings)
}

export const STATE_COLORS: Record<AppState, StateColors> = {
  idle:      { base: [0.9, 0.4, 0.08], hi: [1.0, 0.55, 0.15], hot: [1.0, 0.7, 0.3] },
  listening: { base: [0.9, 0.4, 0.08], hi: [1.0, 0.55, 0.15], hot: [1.0, 0.7, 0.3] },
  thinking:  { base: [0.95, 0.45, 0.1], hi: [1.0, 0.6, 0.18], hot: [1.0, 0.75, 0.35] },
  speaking:  { base: [1.0, 0.55, 0.12], hi: [1.0, 0.65, 0.22], hot: [1.0, 0.8, 0.4] },
};

export const STATE_CONFIGS: Record<AppState, StateConfig> = {
  idle:      { intensity: 1.2, speed: 0.6, energy: 1.0, speak: 0.0 },
  listening: { intensity: 1.3, speed: 0.6, energy: 1.1, speak: 0.0 },
  thinking:  { intensity: 1.5, speed: 0.8, energy: 1.3, speak: 0.0 },
  speaking:  { intensity: 1.35, speed: 0.6, energy: 1.6, speak: 1.0 },
};
```

---

### `src/store/useAppStore.ts` — Global State

```typescript
import { create } from "zustand";
import type { AppState } from "@/lib/stateConfig";

interface AppStore {
  state: AppState;
  clickThrough: boolean;

  setState: (state: AppState) => void;
  setClickThrough: (enabled: boolean) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  state: "idle",
  clickThrough: false,

  setState: (state) => {
    set({ state });
    window.electronAPI?.setState(state);
  },
  setClickThrough: (enabled) => {
    set({ clickThrough: enabled });
    window.electronAPI?.setClickThrough(enabled);
  },
}));
```

---

### `src/App.tsx` — Root Component

```tsx
import { useEffect } from "react";
import { HologramOrb } from "./components/HologramOrb";
import { TitleBar } from "./components/TitleBar";
import { StatusBar } from "./components/StatusBar";
import { useAppStore } from "./store/useAppStore";

export default function App() {
  const setState = useAppStore((s) => s.setState);

  // Listen for global shortcut from main process
  useEffect(() => {
    window.electronAPI?.onShortcutActivated(() => {
      // Toggle listening state
      const current = useAppStore.getState().state;
      setState(current === "listening" ? "idle" : "listening");
    });
  }, [setState]);

  // Keyboard shortcuts for dev testing
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      switch (e.key) {
        case "1": setState("idle"); break;
        case "2": setState("listening"); break;
        case "3": setState("thinking"); break;
        case "4": setState("speaking"); break;
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [setState]);

  return (
    <div className="relative w-full h-full">
      <TitleBar />
      <HologramOrb />
      <StatusBar />
    </div>
  );
}
```

---

### `src/components/TitleBar.tsx` — Frameless Drag Handle

```tsx
export function TitleBar() {
  return (
    <div className="drag-region fixed top-0 left-0 right-0 h-8 z-50 flex items-center justify-end px-2 gap-1">
      <button
        onClick={() => window.electronAPI?.windowMinimize()}
        className="no-drag w-6 h-6 flex items-center justify-center rounded text-secondary/60 hover:text-primary hover:bg-surface transition-colors text-xs"
      >
        ─
      </button>
      <button
        onClick={() => window.electronAPI?.windowClose()}
        className="no-drag w-6 h-6 flex items-center justify-center rounded text-secondary/60 hover:text-red-400 hover:bg-surface transition-colors text-xs"
      >
        ✕
      </button>
    </div>
  );
}
```

---

### `src/components/StatusBar.tsx` — Bottom Status + Mic

```tsx
import { useAppStore } from "@/store/useAppStore";

const STATE_LABELS: Record<string, string> = {
  idle: "Ready",
  listening: "Listening...",
  thinking: "Processing...",
  speaking: "Speaking...",
};

export function StatusBar() {
  const state = useAppStore((s) => s.state);
  const setState = useAppStore((s) => s.setState);

  return (
    <div className="fixed bottom-4 left-0 right-0 flex flex-col items-center gap-3 z-50">
      {/* Status text */}
      <p className="text-xs tracking-widest uppercase text-secondary/80">
        {STATE_LABELS[state] ?? state}
      </p>

      {/* Mic toggle button */}
      <button
        onClick={() => setState(state === "listening" ? "idle" : "listening")}
        className={`
          w-11 h-11 rounded-full border transition-all duration-300
          flex items-center justify-center text-lg
          ${state === "listening"
            ? "border-accent/80 text-accent bg-accent/10 shadow-[0_0_20px_var(--color-accent-glow)]"
            : "border-secondary/30 text-secondary/60 hover:border-secondary/60 hover:text-secondary"
          }
        `}
      >
        🎤
      </button>
    </div>
  );
}
```

---

### `src/components/HologramOrb.tsx` — WebGL Holographic Core

This is the heart of the app. A full-screen Three.js canvas running the holographic GLSL shader ported from the JARVIS Python renderer. Uses additive blending, raymarched volumetric rings, circuit-board surface texture, particles, and voice pulse rings.

```tsx
"use client";

import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { useRef, useMemo, useEffect } from "react";
import * as THREE from "three";
import { useAppStore } from "@/store/useAppStore";
import { STATE_COLORS, STATE_CONFIGS } from "@/lib/stateConfig";

// ─── Hologram Fragment Shader ────────────────────────────────────────────────
// Ported from JARVIS brain_renderer.py GLSL 3.3 → WebGL2 GLSL 300 es
// Features: circuit-board sphere, hexagonal shell, concentric rings, arc fragments,
//           particle cloud, neural lattice, scan plane, voice pulse rings, core glow

const vertexShader = `
  varying vec2 vUV;
  void main() {
    vUV = uv;
    gl_Position = vec4(position, 1.0);
  }
`;

const fragmentShader = `
  precision highp float;
  varying vec2 vUV;

  uniform vec2  uRes;
  uniform float uT;
  uniform float uInt;
  uniform float uEnergy;
  uniform float uSpeak;

  uniform vec3 uBase;
  uniform vec3 uHi;
  uniform vec3 uHot;

  #define PI  3.14159265
  #define TAU 6.28318530

  // ── Noise ──
  float h11(float p){ return fract(sin(p*127.1)*43758.5); }
  float h21(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5); }

  float vnoise(vec3 p){
    vec3 i=floor(p), f=fract(p);
    f=f*f*(3.-2.*f);
    float n=dot(i,vec3(1,57,113));
    return mix(mix(mix(h11(n),h11(n+1.),f.x),
                   mix(h11(n+57.),h11(n+58.),f.x),f.y),
               mix(mix(h11(n+113.),h11(n+114.),f.x),
                   mix(h11(n+170.),h11(n+171.),f.x),f.y),f.z);
  }

  float fbm(vec3 p){
    float v=0., a=.5;
    for(int i=0;i<4;i++){ v+=a*vnoise(p); p*=2.03; a*=.5; }
    return v;
  }

  // ── Camera ──
  mat3 camMat(vec3 ro){
    vec3 w=normalize(-ro), u=normalize(cross(w,vec3(0,1,0))), v=cross(u,w);
    return mat3(u,v,w);
  }

  mat2 rot(float a){ float c=cos(a),s=sin(a); return mat2(c,-s,s,c); }

  float iSphere(vec3 ro, vec3 rd, float r){
    float b=dot(ro,rd), c=dot(ro,ro)-r*r, disc=b*b-c;
    if(disc<0.0) return -1.0;
    return -b-sqrt(disc);
  }

  // ── Hex Grid ──
  vec3 hexGrid(vec2 uv, float scale){
    uv*=scale;
    vec2 r=vec2(1.0,1.732), h=r*0.5;
    vec2 a=mod(uv,r)-h, b=mod(uv-h,r)-h;
    vec2 gv=(dot(a,a)<dot(b,b))?a:b;
    float cellDist=max(abs(gv.x),abs(gv.y*0.577+abs(gv.x)*0.5));
    float edgeLine=smoothstep(0.42,0.46,cellDist)*(1.0-smoothstep(0.46,0.50,cellDist));
    float id=h21(floor(uv/r));
    return vec3(edgeLine,cellDist,id);
  }

  // ── Circuit Board Surface ──
  float circuitBoard(vec2 uv, float t){
    float result=0.0;
    // City blocks
    vec2 g1=uv*45.0; vec2 c1=floor(g1); vec2 f1=fract(g1); float id1=h21(c1);
    if(id1>0.65){
      float rx=smoothstep(0.08,0.12,f1.x)*smoothstep(0.92,0.88,f1.x);
      float ry=smoothstep(0.08,0.12,f1.y)*smoothstep(0.92,0.88,f1.y);
      float br=id1*id1*(0.3+0.7*sin(t*(1.0+id1*3.0)+id1*TAU));
      result+=rx*ry*br*0.7;
    }
    // Fine dots
    vec2 g2=uv*90.0; vec2 c2=floor(g2); vec2 f2=fract(g2); float id2=h21(c2+100.0);
    if(id2>0.75){ result+=exp(-length(f2-0.5)*10.0)*id2*0.45; }
    // Traces
    vec2 g3=uv*30.0; vec2 c3=floor(g3); vec2 f3=fract(g3);
    float id3h=h21(c3+200.0), id3v=h21(c3+300.0);
    if(id3h>0.7){ result+=exp(-abs(f3.y-0.5)*25.0)*0.35*(sin(uv.x*120.0-t*4.0+id3h*20.0)*0.5+0.5)*id3h; }
    if(id3v>0.7){ result+=exp(-abs(f3.x-0.5)*25.0)*0.35*(sin(uv.y*120.0-t*3.0+id3v*20.0)*0.5+0.5)*id3v; }
    // Micro dots
    vec2 g4=uv*160.0; vec2 c4=floor(g4); vec2 f4=fract(g4); float id4=h21(c4+500.0);
    if(id4>0.82){ result+=exp(-length(f4-0.5)*14.0)*pow(sin(t*(2.0+id4*6.0)+id4*TAU)*0.5+0.5,3.0)*0.4; }
    return result;
  }

  // ── Ring Band ──
  float ringBand(vec3 p, float r, float w, float t, float seg, float gap, float rs){
    p.xz*=rot(t*rs);
    float d=length(p.xz), rd=abs(d-r), pd=abs(p.y);
    float ring=exp(-rd*rd/(w*w))*exp(-pd*pd/(w*w*2.0));
    float angle=atan(p.z,p.x);
    float s=smoothstep(gap,gap+0.08,sin(angle*seg)*0.5+0.5);
    float edge=exp(-abs(rd-w*0.5)*300.0)*0.25;
    float dp=pow(sin(angle*3.0-t*5.0)*0.5+0.5,8.0)*0.4;
    return (ring+edge+ring*dp)*s;
  }

  // ── Arc Fragment ──
  float arcFrag(vec3 p, float r, float sa, float sp, float w, float tx, float tz, float t, float rs){
    p.yz*=rot(tx); p.xz*=rot(tz); p.xz*=rot(t*rs);
    float d=length(p.xz), rd=abs(d-r), pd=abs(p.y);
    float arc=exp(-rd*rd/(w*w))*exp(-pd*pd/(w*w*2.0));
    float edge=exp(-abs(rd-w*0.3)*200.0)*0.15;
    float angle=atan(p.z,p.x)+PI;
    float inArc=smoothstep(sa-0.05,sa+0.05,angle)*smoothstep(sa+sp+0.05,sa+sp-0.05,angle);
    float fi=smoothstep(sa,sa+0.15,angle)*smoothstep(sa+sp,sa+sp-0.15,angle);
    return (arc+edge)*inArc*fi;
  }

  // ── Particles ──
  float particles(vec3 p, float t){
    float result=0.0, r=length(p);
    for(int l=0;l<12;l++){
      float fl=float(l), lr=0.06+fl*0.028;
      vec3 lp=p; float rd=mod(fl,2.0)<1.0?1.0:-1.0;
      lp.xz*=rot(t*(0.08+fl*0.02)*rd); lp.yz*=rot(fl*0.4+t*0.025*rd);
      float llr=length(lp); if(llr<0.001) continue;
      vec3 ln=lp/llr;
      float theta=acos(clamp(ln.y,-1.0,1.0)), phi=atan(ln.z,ln.x);
      vec2 cell=floor(vec2(theta*(20.0+fl*6.0),phi*(12.0+fl*4.0)));
      float phase=h21(cell+fl*100.0); if(phase<0.4) continue;
      vec2 off=vec2(h21(cell*1.3+7.0),h21(cell*2.1+13.0))-0.5;
      vec2 fc=fract(vec2(theta*(20.0+fl*6.0),phi*(12.0+fl*4.0)))-0.5-off*0.3;
      float dist=dot(fc,fc);
      float tw=pow(sin(t*(1.5+phase*4.0)+phase*TAU)*0.5+0.5,4.0);
      float rF=exp(-(r-lr)*(r-lr)*400.0);
      result+=tw*(exp(-dist*600.0)*1.2+exp(-dist*80.0)*0.15)*rF*phase*0.6;
    }
    return result;
  }

  // ── Voice Pulse ──
  float voicePulse(vec3 p, float t){
    if(uSpeak<0.01) return 0.0;
    float r=length(p), result=0.0;
    for(int i=0;i<3;i++){
      float wave=fract(t*0.7+float(i)*0.33), wR=wave*0.45;
      float rd=abs(r-wR);
      float ring=exp(-rd*rd*2000.0);
      float glow=exp(-rd*40.0)*0.3;
      float fade=(1.0-wave)*(1.0-wave)*smoothstep(0.0,0.08,wave);
      result+=(ring*0.7+glow)*fade;
    }
    return result*uSpeak;
  }

  void main(){
    vec2 uv=(gl_FragCoord.xy-uRes*0.5)/min(uRes.x,uRes.y);
    float screenR=length(uv);
    if(screenR>0.45){ gl_FragColor=vec4(0.0); return; }

    float t=uT;
    float pulse=1.0+0.05*sin(t*TAU)*uEnergy;
    float flicker=1.0+0.02*sin(t*7.0*TAU)*sin(t*4.37*TAU);
    float holoI=1.0+0.03*sin(uv.y*200.0+t*2.0);
    float bright=uInt*pulse*flicker*holoI;

    float camAng=t*0.22;
    vec3 ro=vec3(sin(camAng)*3.5,sin(t*0.3)*0.15,cos(camAng)*3.5);
    mat3 cam=camMat(ro);
    vec3 rd=cam*normalize(vec3(uv,1.0/tan(22.0*PI/180.0)));

    vec3 col=vec3(0.0); float alpha=0.0;
    float R=0.30;

    // Surface layers
    float tHit=iSphere(ro,rd,R);
    if(tHit>0.0){
      vec3 hp=ro+rd*tHit, N=normalize(hp);
      float th=acos(clamp(N.y,-1.0,1.0)), ph=atan(N.z,N.x);
      vec2 sUV=vec2(ph/TAU+0.5,th/PI); sUV.x+=t*0.02;
      float detail=circuitBoard(sUV,t);
      float fresnel=pow(1.0-abs(dot(N,normalize(-ro))),3.0);
      col+=mix(uBase,mix(uHi,uHot,detail),detail)*detail*2.5*bright;
      col+=mix(uHi,uHot,0.3)*fresnel*0.5*bright;
      alpha+=(detail*1.6+fresnel*0.5)*bright;
    }

    // Inner sphere
    float tH2=iSphere(ro,rd,R*0.65);
    if(tH2>0.0){
      vec3 hp2=ro+rd*tH2, N2=normalize(hp2);
      float th2=acos(clamp(N2.y,-1.0,1.0)), ph2=atan(N2.z,N2.x);
      vec2 sUV2=vec2(ph2/TAU+0.5,th2/PI); sUV2.x-=t*0.015;
      float d2=circuitBoard(sUV2*0.8+10.0,t*0.7);
      col+=mix(uHot,uHi,0.3)*d2*0.75*bright;
      alpha+=d2*0.5*bright;
    }

    // Hex shell
    float tH3=iSphere(ro,rd,R*1.25);
    if(tH3>0.0){
      vec3 hp3=ro+rd*tH3, N3=normalize(hp3);
      float th3=acos(clamp(N3.y,-1.0,1.0)), ph3=atan(N3.z,N3.x);
      vec2 sUV3=vec2(ph3/TAU+0.5,th3/PI); sUV3.x+=t*0.008;
      vec3 hex=hexGrid(sUV3,18.0);
      float hexGlow=0.0;
      if(hex.z>0.7){ hexGlow=pow(sin(t*(1.0+hex.z*3.0)+hex.z*TAU)*0.5+0.5,4.0)*0.25*hex.z; }
      float fr3=pow(1.0-abs(dot(N3,normalize(-ro))),2.0);
      col+=uHi*hex.x*0.4*bright+mix(uBase,uHi,0.4)*hexGlow*1.5*bright+uBase*fr3*0.15*bright;
      alpha+=(hex.x*0.3+hexGlow*0.2+fr3*0.1)*bright;
    }

    // Outer glow
    { float b=dot(ro,rd); float cl=length(ro+rd*max(-b,0.0)); float gd=max(cl-R,0.0);
      if(gd<0.12){ float g=exp(-gd*40.0)*0.10+exp(-gd*100.0)*0.06+exp(-gd*200.0)*0.04;
        col+=uBase*g*bright; alpha+=g*bright*0.25; } }

    // Volumetric (rings, arcs, particles, scan, voice)
    { float sT=max(length(ro)-R*3.5,0.1), eT=length(ro)+R*3.5, dt=(eT-sT)/48.0;
      float aR=0.0,aA=0.0,aP=0.0,aS=0.0,aV=0.0;
      for(int i=0;i<48;i++){
        float rt=sT+dt*(float(i)+0.5); vec3 rp=ro+rd*rt;
        if(length(rp)>R*1.5) continue;
        // Rings
        aR+=ringBand(rp,R*1.35,0.012,t,6.0,0.25,0.04)*dt;
        aR+=ringBand(rp,R*1.25,0.015,t,10.0,0.2,-0.07)*dt;
        aR+=ringBand(rp,R*0.90,0.013,t,12.0,0.15,-0.1)*dt;
        aR+=ringBand(rp,R*0.65,0.012,t,8.0,0.25,-0.08)*dt;
        aR+=ringBand(rp,R*0.48,0.014,t,6.0,0.15,0.18)*dt;
        // Arcs
        aA+=arcFrag(rp,R*1.30,0.3,1.5,0.010,0.4,0.0,t,0.10)*dt;
        aA+=arcFrag(rp,R*1.20,2.0,1.8,0.008,-0.2,0.5,t,-0.08)*dt;
        aA+=arcFrag(rp,R*1.10,4.0,1.2,0.010,0.6,-0.3,t,0.12)*dt;
        aA+=arcFrag(rp,R*0.95,0.8,1.6,0.011,0.3,0.4,t,0.14)*dt;
        aA+=arcFrag(rp,R*0.75,1.5,2.5,0.009,0.7,0.1,t,0.07)*dt;
        aA+=arcFrag(rp,R*0.55,1.2,2.0,0.011,0.5,-0.4,t,0.18)*dt;
        aA+=arcFrag(rp,R*0.40,4.5,1.0,0.012,-0.3,0.7,t,-0.14)*dt;
        // Particles
        aP+=particles(rp,t)*dt*0.8;
        // Scan
        float plY=sin(t*0.7)*0.18, sDist=abs(rp.y-plY);
        aS+=(exp(-sDist*60.0)*0.6+exp(-sDist*15.0)*0.08)*smoothstep(R*1.35,R*0.5,length(rp))*dt;
        // Voice
        aV+=voicePulse(rp,t)*dt;
      }
      vec3 hud=mix(uHi,uHot,0.2)*aR*bright*4.0
              +mix(uBase,uHi,0.4)*aA*bright*3.2
              +mix(uHot,uHi,0.4)*aP*bright*3.0
              +mix(uHi,uHot,0.3)*aS*bright*1.0
              +mix(uHot,vec3(1.0,0.85,0.5),0.3)*aV*bright*2.5;
      col+=hud; alpha+=dot(hud,vec3(0.33))*0.6;
    }

    // Core glow
    { float b=dot(ro,rd); vec3 cp=ro+rd*max(-b,0.0); float cd=length(cp);
      float core=exp(-cd*30.0)*1.4*uEnergy*(1.0+uSpeak*0.3*sin(t*4.5))*(1.0+0.15*sin(t*2.0));
      core*=fbm(cp*15.0+t*0.8)*0.2+0.8;
      float cg=exp(-cd*(18.0-uSpeak*4.0))*(0.25+uSpeak*0.15)*uEnergy;
      col+=mix(uHot,vec3(1.0),0.2)*core*bright*1.5+mix(uBase,uHi,0.5)*cg*bright;
      alpha+=(core*0.6+cg*0.25)*bright;
    }

    // Holographic color correction
    { float lum=dot(col,vec3(0.299,0.587,0.114));
      col=mix(col,vec3(lum),smoothstep(0.6,1.5,lum)*0.15); }

    float lum=dot(col,vec3(0.299,0.587,0.114));
    alpha=clamp(max(alpha,lum),0.0,1.0);
    if(alpha<0.02){ gl_FragColor=vec4(0.0); return; }
    alpha*=smoothstep(0.02,0.06,alpha);
    gl_FragColor=vec4(col,alpha);
  }
`;

// ─── Shader Mesh ─────────────────────────────────────────────────────────────

function HologramMesh() {
  const meshRef = useRef<THREE.Mesh>(null);
  const { size } = useThree();
  const state = useAppStore((s) => s.state);

  // Current interpolated values (lerped each frame)
  const current = useRef({
    base: new THREE.Vector3(...STATE_COLORS.idle.base),
    hi: new THREE.Vector3(...STATE_COLORS.idle.hi),
    hot: new THREE.Vector3(...STATE_COLORS.idle.hot),
    intensity: STATE_CONFIGS.idle.intensity,
    speed: STATE_CONFIGS.idle.speed,
    energy: STATE_CONFIGS.idle.energy,
    speak: STATE_CONFIGS.idle.speak,
  });

  const uniforms = useMemo(() => ({
    uRes: { value: new THREE.Vector2(size.width, size.height) },
    uT: { value: 0 },
    uInt: { value: 1.2 },
    uEnergy: { value: 1.0 },
    uSpeak: { value: 0.0 },
    uBase: { value: new THREE.Vector3(...STATE_COLORS.idle.base) },
    uHi: { value: new THREE.Vector3(...STATE_COLORS.idle.hi) },
    uHot: { value: new THREE.Vector3(...STATE_COLORS.idle.hot) },
  }), []);

  // Update resolution on resize
  useEffect(() => {
    uniforms.uRes.value.set(size.width, size.height);
  }, [size, uniforms]);

  useFrame((_, delta) => {
    const c = current.current;
    const colors = STATE_COLORS[state];
    const config = STATE_CONFIGS[state];
    const lr = 0.04; // lerp rate (smooth transitions)

    // Lerp colors
    c.base.lerp(new THREE.Vector3(...colors.base), lr);
    c.hi.lerp(new THREE.Vector3(...colors.hi), lr);
    c.hot.lerp(new THREE.Vector3(...colors.hot), lr);

    // Lerp parameters
    c.intensity += (config.intensity - c.intensity) * lr;
    c.speed += (config.speed - c.speed) * lr;
    c.energy += (config.energy - c.energy) * lr;
    // Speak: fast ramp up (0.12), slow fade (0.03)
    const spkLr = config.speak > c.speak ? 0.12 : 0.03;
    c.speak += (config.speak - c.speak) * spkLr;

    // Update uniforms
    uniforms.uT.value += delta * c.speed;
    uniforms.uInt.value = c.intensity;
    uniforms.uEnergy.value = c.energy;
    uniforms.uSpeak.value = c.speak;
    uniforms.uBase.value.copy(c.base);
    uniforms.uHi.value.copy(c.hi);
    uniforms.uHot.value.copy(c.hot);
  });

  return (
    <mesh ref={meshRef}>
      <planeGeometry args={[2, 2]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </mesh>
  );
}

// ─── Canvas Wrapper ──────────────────────────────────────────────────────────

export function HologramOrb() {
  return (
    <div className="fixed inset-0 z-0">
      <Canvas
        orthographic
        camera={{ zoom: 1, position: [0, 0, 1] }}
        gl={{ alpha: true, antialias: false, premultipliedAlpha: false }}
        style={{ background: "transparent" }}
      >
        <HologramMesh />
      </Canvas>
    </div>
  );
}
```

---

### `vite.config.ts`

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import electron from "vite-plugin-electron";
import renderer from "vite-plugin-electron-renderer";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    electron([
      {
        entry: "electron/main.ts",
        vite: {
          build: { outDir: "dist-electron" },
        },
      },
      {
        entry: "electron/preload.ts",
        onstart({ reload }) { reload(); },
        vite: {
          build: { outDir: "dist-electron" },
        },
      },
    ]),
    renderer(),
  ],
  resolve: {
    alias: { "@": path.resolve(__dirname, "src") },
  },
});
```

---

## Scaffolding Checklist

When invoked, generate files in this order:

1. `package.json` — dependencies from tech stack above + scripts
2. `vite.config.ts` — from template
3. `tsconfig.json` + `electron/tsconfig.json`
4. `src/index.html` — from template
5. `src/globals.css` — from template
6. `src/main.tsx` — from template
7. `src/types/electron.d.ts` — IPC type declarations
8. `src/lib/stateConfig.ts` — from template (state colors + configs)
9. `src/store/useAppStore.ts` — from template
10. `electron/main.ts` — from template
11. `electron/preload.ts` — from template
12. `src/App.tsx` — from template
13. `src/components/TitleBar.tsx` — from template
14. `src/components/StatusBar.tsx` — from template
15. `src/components/HologramOrb.tsx` — from template (the full shader)

Then `npm install` and `npm run dev` to launch the holographic Electron app.

## Design Direction

- **Hologram IS the UI** — the full-screen shader orb is the primary visual
- **Transparent window** — only the glowing hologram is visible, desktop shows through
- **Additive blending** — bright colors glow on dark/transparent background
- **State-driven** — all visuals respond to idle/listening/thinking/speaking
- **Minimal chrome** — tiny title bar buttons, small status text, mic toggle
- **Orange/gold palette** — warm Iron Man JARVIS tones (customizable)

## State Machine

```
idle (orange, calm)
  ↓ user activates
listening (orange, slightly brighter)
  ↓ input received
thinking (warmer orange, faster, higher energy)
  ↓ response ready
speaking (golden, voice pulse rings active)
  ↓ done
idle
```

All transitions use lerp (rate: 0.04) for smooth, cinematic color blending.
Speak pulse: fast ramp up (0.12), slow graceful fade (0.03).

## What To Ask The User

Before building, gather:
- **App name** and purpose (AI assistant, system monitor, music player, etc.)
- **Accent color preference** — Jarvis orange (default) or custom
- **Window size** — default 800x800
- **Global shortcut** — default Ctrl+Alt+J
- **Backend integration** — will it connect to an API, local LLM, or standalone?

If not provided, use the Jarvis orange defaults with an 800x800 window.
