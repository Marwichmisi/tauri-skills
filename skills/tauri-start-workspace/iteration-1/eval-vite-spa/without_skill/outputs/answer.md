# Démarrer un projet Tauri v2 + Vite + React (pnpm)

## 1. Prérequis

- Rust stable (via rustup) + toolchain MSVC sur Windows
- Node LTS + pnpm : `corepack enable && corepack prepare pnpm@latest --activate`
- Linux : `libwebkit2gtk`, `build-essential`, `curl`, etc. (voir `tauri doctor`)

Vérification :

```bash
rustc --version
node --version
pnpm --version
pnpm dlx @tauri-apps/cli --version
```

## 2. Scaffold

Option interactive (recommandée) :

```bash
pnpm create tauri-app@latest
# template: React + TypeScript (+ Vite intégré)
cd mon-app
pnpm install
```

Option non-interactive :

```bash
pnpm create tauri-app@latest mon-app -- --template react-ts --manager pnpm
cd mon-app
pnpm install
```

Lanceur obtenu (`package.json`) :

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "tauri": "tauri"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "@tauri-apps/api": "^2"
  },
  "devDependencies": {
    "@tauri-apps/cli": "^2",
    "vite": "^6",
    "typescript": "~5.6"
  }
}
```

Dev / build :

```bash
pnpm tauri dev     # = beforeDevCommand + tauri dev
pnpm tauri build  # = beforeBuildCommand + tauri build
pnpm tauri doctor # diagnostic
```

## 3. tauri.conf.json (build) — SPA Vite + React

Fichier complet minimal v2, adapté à Vite (`dist/`). Le fichier de référence est aussi livré à part (`tauri.conf.json`).

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "mon-app",
  "version": "0.1.0",
  "identifier": "com.example.monapp",
  "build": {
    "devUrl": "http://localhost:1420",
    "frontendDist": "../dist",
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build"
  },
  "app": {
    "windows": [
      {
        "title": "mon-app",
        "width": 800,
        "height": 600
      }
    ],
    "security": {
      "csp": null
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

Points clés :

- `build.devUrl` doit pointer exactement sur `server.port` de Vite (ici `1420`).
- `build.frontendDist` = sortie Vite relative à `src-tauri/` → `../dist` par défaut Vite. Si `vite.config.ts` définit `build.outDir: "dist"` ne rien changer. Ne pas mettre `../src` ni `../build` (sauf CRA).
- `beforeDevCommand` / `beforeBuildCommand` utilisent `pnpm` (pas `npm`).
- En mobile (`android`/`ios`), passer par `tauri init` / `tauri android init` qui ajoute `src/lib.rs` — ne pas éditer `tauri.conf.json` à la main pour ça.

## 4. Rappel vite.config.ts

Config canonique recommandée par Tauri v2 pour Vite + React :

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const host = process.env.TAURI_DEV_HOST;

// https://v2.tauri.app/start/frontend/vite/
export default defineConfig(async () => ({
  plugins: [react()],

  // Évite d'effacer la sortie Rust dans le terminal
  clearScreen: false,

  server: {
    port: 1420,
    strictPort: true, // échoue si 1420 occupé au lieu de switcher -> devUrl reste valide
    host: host || false, // TAURI_DEV_HOST pour dev LAN / mobile
    hmr: host
      ? {
          protocol: "ws",
          host,
          port: 1421,
        }
      : undefined,
    watch: {
      // ignore src-tauri/ -> évite les reloads infinis quand Rust recompile
      ignored: ["**/src-tauri/**"],
    },
  },

  envPrefix: ["VITE_", "TAURI_ENV_*"],

  build: {
    // Tauri utilise Chromium moderne / WebKit
    target:
      process.env.TAURI_ENV_PLATFORM == "windows" ? "chrome105" : "safari13",
    // déjà `dist/` par défaut, à aligner avec frontendDist
    // outDir: "dist",
    minify: !process.env.TAURI_ENV_DEBUG ? "esbuild" : false,
    sourcemap: !!process.env.TAURI_ENV_DEBUG,
  },
}));
```

Pourquoi ces 3 réglages :

1. `strictPort: true` — garantit que `devUrl: http://localhost:1420` reste correct. Sans ça Vite bascule sur 1421 silencieusement et la WebView ouvre une page vide.
2. `watch.ignored: ["**/src-tauri/**"]` — sinon chaque `cargo build` touche `src-tauri/target/` et relance Vite en boucle.
3. `host: TAURI_DEV_HOST` + `hmr` — obligatoire pour `pnpm tauri dev --host` et dev Android/iOS sur device physique. Sans ça le téléphone ne peut pas joindre le dev-server ni le HMR.

## 5. Arborescence src-tauri/ attendue (Tauri v2)

```
src-tauri/
├── Cargo.toml              # manifest Rust, deps tauri v2
├── tauri.conf.json         # config ci-dessus
├── build.rs                # tauri_build::build()
├── src/
│   ├── main.rs             # entrée desktop : tauri::Builder + run
│   └── lib.rs              # requis si mobile (android/ios), sinon optionnel
├── capabilities/
│   └── default.json        # permissions v2 (core/fs/dialog/http...)
├── icons/
│   ├── 32x32.png
│   ├── 128x128.png
│   ├── 128x128@2x.png
│   ├── icon.icns
│   └── icon.ico
└── gen/
    └── schemas/            # généré par le CLI, ne pas éditer à la main
```

Détails :

- `Cargo.toml` minimal :
  ```toml
  [package]
  name = "mon-app"
  version = "0.1.0"
  edition = "2021"

  [build-dependencies]
  tauri-build = { version = "2", features = [] }

  [dependencies]
  tauri = { version = "2", features = [] }
  serde = { version = "1", features = ["derive"] }
  serde_json = "1"
  ```
- `build.rs` minimal :
  ```rust
  fn main() {
      tauri_build::build()
  }
  ```
- `src/main.rs` minimal :
  ```rust
  #![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

  fn main() {
      mon_app_lib::run()
  }
  ```
  avec `src/lib.rs` exposant `run()` + `Builder::invoke_handler`. En pur desktop le template simple met tout dans `main.rs` sans `lib.rs` — les deux sont valides, `lib.rs` devient obligatoire dès que `tauri android|ios init` est utilisé.
- `capabilities/default.json` (nouveau en v2, remplace `allowlist` v1) :
  ```json
  {
    "$schema": "../gen/schemas/desktop-schema.json",
    "identifier": "default",
    "description": "Capability for the main window",
    "windows": ["main"],
    "permissions": ["core:default", "opener:default"]
  }
  ```
  Référencé depuis `tauri.conf.json` via `"app": { "security": { "capabilities": ["default"] } }` selon template (ou implicite). Ajouter `fs:default`, `dialog:default`, `http:default` au besoin via `pnpm tauri add fs` plutôt qu'à la main.
- `tauri.conf.json` reste à la racine de `src-tauri/`, `frontendDist` relatif à ce dossier.
- Ne jamais commiter `src-tauri/target/` ni `gen/` custom — `target/` ignoré via `.gitignore`.

## 6. Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| WebView blanche en `dev` | port Vite ≠ `devUrl` | `strictPort: true` + `port: 1420` |
| Reload infini | Vite watch `src-tauri/` | `watch.ignored: ["**/src-tauri/**"]` |
| `frontendDist` introuvable en `build` | `outDir` ≠ `../dist` | aligner `frontendDist` et `build.outDir` |
| Device mobile ne charge pas | `host: false` | `host: TAURI_DEV_HOST \|\| false` + `--host` |
| Commande Tauri bloquée | capability manquante v2 | ajouter permission + `pnpm tauri add <plugin>` |
