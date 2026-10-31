# Frontends meta (Next/Nuxt/SvelteKit/Qwik) — extraits doc

Commit `ec113a50`, EN canonique. Règle commune (voir `frontend-vite.md`) : Tauri ne supporte pas le serveur (SSR) — SSG/SPA seuls. Mobile exige serveur dev joignable sur IP interne.

## Next.js

Source : `tauri-docs/src/content/docs/start/frontend/nextjs.mdx` (titre `Next.js`, exact à 14.2.3).

Checklist (même fichier) :
- Use static exports by setting `output: 'export'`. Tauri doesn't support server-based solutions.
- Use the `out` directory as `frontendDist` in `tauri.conf.json`.

Config Tauri (onglet pnpm ; npm/yarn/deno identiques) — voir `examples/tauri.conf.nextjs.json` :

```json
{ "build": { "beforeDevCommand": "pnpm dev", "beforeBuildCommand": "pnpm build", "devUrl": "http://localhost:3000", "frontendDist": "../out" } }
```

Config Next (même fichier) :

```ts
// next.config.mjs
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  assetPrefix: isProd ? undefined : `http://${internalHost}:3000`,
};
```

## Nuxt

Source : `tauri-docs/src/content/docs/start/frontend/nuxt.mdx` (titre `Nuxt`, exact à 4.2).

Checklist (même fichier) :
- Use SSG by setting `ssr: false`. Tauri doesn't support server based solutions.
- Use default `../dist` as `frontendDist` in `tauri.conf.json`.
- Compile using `nuxi build`.
- (Optional): `telemetry: false`.

Config Tauri — voir `examples/tauri.conf.nuxt.json` (note `generate`, pas `build`) :

```json
{ "build": { "beforeDevCommand": "pnpm dev", "beforeBuildCommand": "pnpm generate", "devUrl": "http://localhost:3000", "frontendDist": "../dist" } }
```

Config Nuxt (même fichier) :

```ts
export default defineNuxtConfig({
  ssr: false,
  devServer: { host: '0' },
  vite: { clearScreen: false, envPrefix: ['VITE_', 'TAURI_'], server: { strictPort: true } },
  ignore: ['**/src-tauri/**'],
});
```

Le check échoue si `beforeBuildCommand` ne contient pas `generate` (`--frontend nuxt`).

## SvelteKit

Source : `tauri-docs/src/content/docs/start/frontend/sveltekit.mdx` (titre `SvelteKit`, exact à SvelteKit 2.20.4 / Svelte 5.25.8).

Checklist (même fichier) :
- Use SSG + SPA via `static-adapter`. Tauri doesn't support server-based solutions.
- SPA sans prerender recommandé (`load` sans API Tauri au build sinon).
- Use `build/` as `frontendDist` in `tauri.conf.json`.

Config Tauri — voir `examples/tauri.conf.sveltekit.json` :

```json
{ "build": { "beforeDevCommand": "pnpm dev", "beforeBuildCommand": "pnpm build", "devUrl": "http://localhost:5173", "frontendDist": "../build" } }
```

Config SvelteKit (même fichier) : `npm install --save-dev @sveltejs/adapter-static`, `adapter: adapter({ fallback: 'index.html' })`, puis `src/routes/+layout.ts` avec `export const ssr = false;`.

## Qwik

Source : `tauri-docs/src/content/docs/start/frontend/qwik.mdx` (titre `Qwik`).

Checklist (même fichier) :
- Use SSG. Tauri doesn't support server-based solutions.
- Use `dist/` as `frontendDist` in `tauri.conf.json`.

Séquence (même fichier) : `create qwik`, `qwik add static`, installer `@tauri-apps/cli`, `tauri init`, config Tauri `devUrl http://localhost:5173` + `frontendDist ../dist` + dev/build, puis `tauri dev`.
