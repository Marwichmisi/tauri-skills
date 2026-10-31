# SvelteKit SPA sans prerender pour Tauri v2 (pnpm)

## 1. Install adapter-static

```bash
pnpm add -D @sveltejs/adapter-static
```

Vérifier dans `package.json` :
```json
{
  "devDependencies": {
    "@sveltejs/adapter-static": "^3.0.0",
    "@sveltejs/kit": "^2.0.0"
  }
}
```

## 2. `tauri.conf.json` (src-tauri/tauri.conf.json)

`frontendDist` pointe sur `../build` (sortie SvelteKit à la racine du projet) :

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "tauri-app",
  "version": "0.1.0",
  "identifier": "com.tauri.app",
  "build": {
    "frontendDist": "../build",
    "devUrl": "http://localhost:5173",
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build"
  },
  "app": {
    "windows": [
      {
        "title": "Tauri App",
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

> Fichier complet aussi livré dans `tauri.conf.json`.
> Points clés Tauri v2 : `build.frontendDist` (pas `build.distDir` v1), `build.devUrl` + `beforeDevCommand` / `beforeBuildCommand` pour pnpm.

## 3. `svelte.config.js`

```js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: 'index.html',
      precompress: false,
      strict: false
    })
  }
};

export default config;
```

Pourquoi :
- `pages` / `assets`: `build` → correspond à `../build` vu depuis `src-tauri/`.
- `fallback: 'index.html'` : mode SPA. Le routeur SvelteKit prend le relais côté client, aucune page n'a besoin d'être pré-rendue.
- `strict: false` : ne fait pas échouer le build si une route n'est pas pré-rendue (indispensable en SPA sans prerender).

## 4. `src/routes/+layout.ts`

```ts
export const ssr = false;
```

- `ssr = false` force le rendu 100% client (CSR), compatible `tauri://` / fichiers locaux sans serveur Node.
- Pas de `export const prerender = true` : on est volontairement en SPA sans prerender. Le `fallback: 'index.html'` de l'adapter couvre le routage.
- Fichier à placer exactement à `src/routes/+layout.ts` (pas `.js`, pour que `ssr:false` s'applique à toutes les routes).

Optionnel si avertissement SvelteKit sur le prerender :
```ts
export const prerender = false;
export const ssr = false;
```

## 5. Vérification structure

Structure attendue :

```
projet/
  package.json          # scripts dev/build + adapter-static en devDeps
  svelte.config.js      # adapter-static + fallback index.html
  vite.config.ts        # plugin sveltekit(), server.strictPort true si besoin
  src/
    routes/
      +layout.ts        # ssr = false
      +page.svelte
  static/
  build/                # généré par `pnpm build`, servi par Tauri
  src-tauri/
    tauri.conf.json     # frontendDist ../build
    icons/
    capabilities/
```

Commandes de vérification :

```bash
# 1. Fichiers requis
test -f svelte.config.js && echo "ok svelte.config"
test -f src/routes/+layout.ts && echo "ok layout"
test -f src-tauri/tauri.conf.json && echo "ok tauri conf"

# 2. Contenu clé
grep -q "adapter-static" svelte.config.js && echo "ok adapter"
grep -q "fallback" svelte.config.js && echo "ok fallback"
grep -q "ssr = false" src/routes/+layout.ts && echo "ok ssr false"
grep -q '"frontendDist": "../build"' src-tauri/tauri.conf.json && echo "ok frontendDist"

# 3. Build web seul (doit produire build/index.html)
pnpm build
test -f build/index.html && echo "ok build SPA"
```

Si `pnpm build` échoue avec erreur adapter-static `strict` / prerender, vérifier `strict: false` + `fallback` + absence de `prerender = true`.
