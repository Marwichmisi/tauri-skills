# SvelteKit SPA sans prerender — Tauri v2 (pnpm)

Sources : `tauri-docs` local, commit `ec113a50`, EN canonique seule.
- `src/content/docs/start/frontend/sveltekit.mdx` (titre `SvelteKit`, SvelteKit 2.20.4 / Svelte 5.25.8) via `skills/tauri-start/references/frontend-meta.md`
- `src/content/docs/start/project-structure.mdx` (titre `Project Structure`) via `references/project-structure.md`
- `src/content/docs/start/frontend/index.mdx` (règle commune, via `references/frontend-vite.md`)

Règle commune : Tauri agit comme hôte statique, pas de serveur. SSG/SPA seuls, pas de SSR.

## 1. `src-tauri/tauri.conf.json` (bloc `build`, pnpm)

Valeurs documentées seules : `frontendDist ../build`, `devUrl :5173`.

```json
{
  "build": {
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../build"
  }
}
```

Copie de `examples/tauri.conf.sveltekit.json`.

## 2. SvelteKit SPA sans prerender

Checklist doc (sveltekit.mdx) :
- Use SSG + SPA via `static-adapter`. Tauri doesn't support server-based solutions.
- SPA sans prerender recommandé (`load` sans API Tauri au build sinon).
- Use `build/` as `frontendDist`.

Install (même fichier) :

```sh
npm install --save-dev @sveltejs/adapter-static
```

`svelte.config.js` (même fichier) :

```js
adapter: adapter({ fallback: 'index.html' })
```

`src/routes/+layout.ts` (même fichier) :

```ts
export const ssr = false;
```

## 3. Structure `src-tauri/` attendue

Voir `examples/project-structure.txt` (copie exacte de l'arbre doc) :

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

## 4. Checks

Frontend :

```sh
python3 scripts/check-start.py src-tauri/tauri.conf.json --frontend sveltekit
```

Structure (vérifie les 5 fichiers requis `Cargo.toml`, `build.rs`, `main.rs`, `lib.rs`, `tauri.conf.json`) :

```sh
python3 scripts/check-start.py src-tauri/tauri.conf.json --project-root .
```

Résultat sur la conf produite (`outputs/tauri.conf.json`) :

```
OK /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start-workspace/iteration-1/eval-sveltekit-spa/with_skill/outputs/tauri.conf.json: frontend=sveltekit, frontendDist=../build, devUrl=http://localhost:5173
```

## 5. Frontière

Schéma complet `tauri.conf.json` / `gen/schemas` et CLI (`tauri init/dev/build`, `tauri icon`) : skill `tauri-config-cli-reference`. Ici seul le bloc `build` documenté par frontend est montré (doctrine `tauri-start` SKILL.md § Frontières).
