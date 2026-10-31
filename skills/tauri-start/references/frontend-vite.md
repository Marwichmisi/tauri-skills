# Frontend Vite — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/start/frontend/index.mdx` (titre `Frontend Configuration`)
- `tauri-docs/src/content/docs/start/frontend/vite.mdx` (titre `Vite`, guide exact à Vite 8)

## Checklist frontend (index.mdx, s'applique à tous)

> Conceptually Tauri acts as a static web host. You need to provide Tauri with a folder containing some mix of HTML, CSS, Javascript and possibly WASM that can be served to the webview Tauri provides.

- Use static site generation (SSG), single-page applications (SPA), or classic multi-page apps (MPA). Tauri does not natively support server based alternatives (such as SSR).
- For mobile development, a development server of some kind is necessary that can host the frontend on your internal IP.
- Use a proper client-server relationship (no hybrid SSR).

> For most projects we recommend [Vite](https://vitejs.dev/) for SPA frameworks such as React, Vue, Svelte, and Solid, but also for plain JavaScript or TypeScript projects.

Si framework absent de la liste : il marche souvent sans config ; relire la checklist ci-dessus.

## Checklist Vite (vite.mdx)

- Use `../dist` as `frontendDist` in `src-tauri/tauri.conf.json`.
- Use `process.env.TAURI_DEV_HOST` as the development server host IP when set to run on iOS physical devices.

## Config Tauri (vite.mdx, onglet pnpm ; npm/yarn/deno identiques au port près)

Voir `examples/tauri.conf.vite.json` (copie exacte du bloc pnpm) :

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

`package.json` supposé (même fichier) : `"dev": "vite"`, `"build": "tsc && vite build"`, `"preview": "vite preview"`, `"tauri": "tauri"`.

## Config Vite (vite.mdx)

Voir `examples/vite.config.example.js` (copie exacte, commentaires doc conservés) :

- `clearScreen: false` (ne pas masquer les erreurs Rust).
- `server.port: 5173` + `strictPort: true` (doit matcher `devUrl`).
- `host: host || false` + `hmr` ws sur `TAURI_DEV_HOST` (iOS physique).
- `watch.ignored: ['**/src-tauri/**']`.
- `envPrefix: ['VITE_', 'TAURI_ENV_*']`.
- `build.target` : `chrome105` (windows) sinon `safari13` ; `minify`/`sourcemap` selon `TAURI_ENV_DEBUG`.

Check : `python3 scripts/check-start.py examples/tauri.conf.vite.json --frontend vite`.
