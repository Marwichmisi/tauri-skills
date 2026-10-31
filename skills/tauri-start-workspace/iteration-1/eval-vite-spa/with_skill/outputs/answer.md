# Démarrage Tauri v2 + Vite + React (pnpm)

## 1. Scaffolding

Option recommandée (`references/create-project.md`) :
```sh
cd tauri-app
pnpm install
pnpm tauri dev
```
Via `create-tauri-app` : langage `TypeScript / JavaScript`, package manager `pnpm`, template `React`.
Setup manuel : `pnpm create vite .`, `pnpm add -D @tauri-apps/cli@latest`, `pnpm tauri init` (web assets `..`, dev server `http://localhost:5173`, dev `pnpm run dev`, build `pnpm run build`).

Prérequis (`references/prerequisites.md`) : dépendances système (Linux `libwebkit2gtk-4.1-dev`, macOS Xcode, Windows C++ Build Tools + WebView2), Rust via rustup, Node LTS (`node -v` / `npm -v`, `corepack enable` pour pnpm). Mobile seulement si Android/iOS.

## 2. `src-tauri/tauri.conf.json` — bloc `build` (Vite + pnpm)

Copie exacte de `examples/tauri.conf.vite.json` :

```json
{
  "build": {
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  }
}
```

Règles : `frontendDist` = `../dist`, `devUrl` port `:5173`. `package.json` supposé : `"dev": "vite"`, `"build": "tsc && vite build"`, `"preview": "vite preview"`, `"tauri": "tauri"`.

## 3. Rappel `vite.config` (copie exacte `examples/vite.config.example.js`)

```js
import { defineConfig } from 'vite';

const host = process.env.TAURI_DEV_HOST;

export default defineConfig({
  clearScreen: false,
  server: {
    port: 5173,
    strictPort: true,
    host: host || false,
    hmr: host ? { protocol: 'ws', host, port: 1421 } : undefined,
    watch: { ignored: ['**/src-tauri/**'] },
  },
  envPrefix: ['VITE_', 'TAURI_ENV_*'],
  build: {
    target: process.env.TAURI_ENV_PLATFORM == 'windows' ? 'chrome105' : 'safari13',
    minify: !process.env.TAURI_ENV_DEBUG,
    sourcemap: !!process.env.TAURI_ENV_DEBUG,
  },
});
```

Points exigés :
- `strictPort: true` + `server.port: 5173` (doit matcher `devUrl`).
- `watch.ignored: ['**/src-tauri/**']` (évite les rebuilds en boucle).
- `host: host || false` + HMR ws sur `TAURI_DEV_HOST` (iOS physique, serveur dev joignable sur IP interne).
- `clearScreen: false` (ne pas masquer erreurs Rust), `envPrefix`, `build.target` selon plateforme.

## 4. Arborescence `src-tauri/` attendue (copie exacte `examples/project-structure.txt`)

```
.
├── package.json
├── index.html
├── src/
│   ├── main.js
├── src-tauri/
│   ├── Cargo.toml
│   ├── Cargo.lock
│   ├── build.rs
│   ├── tauri.conf.json
│   ├── src/
│   │   ├── main.rs
│   │   └── lib.rs
│   ├── icons/
│   │   ├── icon.png
│   │   ├── icon.icns
│   │   └── icon.ico
│   └── capabilities/
│       └── default.json
```

Rôles : `tauri.conf.json` config principale + marqueur CLI ; `capabilities/` capability files ; `icons/` sortie `tauri icon` ; `build.rs` = `tauri_build::build()` ; `src/lib.rs` code Rust + entrée mobile (`#[cfg_attr(mobile, tauri::mobile_entry_point)]`) ; `src/main.rs` entrée desktop appelant `app_lib::run()`, ne pas modifier.

Principe : Tauri = hôte statique (SSG/SPA/MPA seuls, pas de SSR). Compiler le JS en fichiers statiques d'abord, puis le Rust qui les bundle.

## 5. Validation `scripts/check-start.py`

Commande :
```
python3 /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start/scripts/check-start.py <outputs>/tauri.conf.json --frontend vite
```

Résultat :
```
OK /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start-workspace/iteration-1/eval-vite-spa/with_skill/outputs/tauri.conf.json: frontend=vite, frontendDist=../dist, devUrl=http://localhost:5173
```

Aucune valeur inventée : seuls `../dist` / `:5173` pour Vite.

## 6. Sources (EN canonique seule, commit `ec113a50`)

- `tauri-docs/src/content/docs/start/frontend/index.mdx` (titre `Frontend Configuration`)
- `tauri-docs/src/content/docs/start/frontend/vite.mdx` (titre `Vite`, guide exact à Vite 8)
- `tauri-docs/src/content/docs/start/project-structure.mdx` (titre `Project Structure`)
- `tauri-docs/src/content/docs/start/create-project.mdx` (titre `Create a Project`)
- `tauri-docs/src/content/docs/start/prerequisites.mdx` (titre `Prerequisites`)
- `tauri-docs/src/content/docs/start/index.mdx` (titre `What is Tauri?`, § Why Tauri)
