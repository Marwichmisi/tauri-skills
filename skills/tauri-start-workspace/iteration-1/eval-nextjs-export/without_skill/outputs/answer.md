# Next.js existant + Tauri v2 (pnpm) — mode statique uniquement

## 1. `next.config.mjs` minimale (pas de SSR)

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
```

Points obligatoires :
- `output: 'export'` : force `pnpm build` à générer du statique dans `./out/`. Pas de serveur Node, donc pas de SSR.
- `images.unoptimized: true` : `next/image` Optimization API nécessite un serveur. En statique, on la désactive.
- Ne pas utiliser en mode export : `getServerSideProps`, Route Handlers / API Routes, `middleware` avec rewrite dynamique, `next/headers`, `cookies()` / `draftMode` dynamique. Remplacer par `getStaticProps` / composants statiques.
- Si liens internes : privilégier `trailingSlash: true` optionnel pour compatibilité file-system, mais pas obligatoire.

## 2. `tauri.conf.json` minimale (Tauri v2)

Placée dans `src-tauri/tauri.conf.json` :

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "my-app",
  "version": "0.1.0",
  "identifier": "com.example.my-app",
  "build": {
    "frontendDist": "../out",
    "devUrl": "http://localhost:3000",
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build"
  },
  "app": {
    "windows": [
      {
        "title": "my-app",
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

Explications :
- `build.frontendDist: "../out"` : chemin relatif depuis `src-tauri/` vers l'export Next.js.
- `build.devUrl: "http://localhost:3000"` : `pnpm dev` Next.js par défaut.
- `beforeDevCommand: "pnpm dev"`, `beforeBuildCommand: "pnpm build"` : intégration pnpm.
- `app.security.csp: null` : évite les blocages CSP en dev avec Next.js (à durcir en prod si besoin).
- Adapter `identifier` (format `com.org.app`, unique) et `productName`.

Voir aussi fichier `tauri.conf.json` livré à côté de cette réponse.

## 3. Commandes pnpm

```bash
pnpm add -D @tauri-apps/cli
pnpm dlx tauri init --ci # déjà fait si src-tauri existe, sinon manuel
pnpm dev          # Next.js seul
pnpm tauri dev    # Next.js dans WebView Tauri
pnpm tauri build  # export statique + bundle desktop
```

Vérification : `pnpm build` doit créer `out/index.html`. `pnpm tauri build` doit le charger sans erreur 404.
