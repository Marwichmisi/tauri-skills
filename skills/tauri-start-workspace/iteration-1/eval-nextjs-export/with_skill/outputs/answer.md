# Next.js existant + Tauri v2 (pnpm) — config statique uniquement, pas de SSR

## 1. `src-tauri/tauri.conf.json` (bloc `build`, minimal)

```json
{
  "build": {
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../out"
  }
}
```

## 2. `next.config.mjs` (minimal, export statique)

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
};

export default nextConfig;
```

## 3. Pourquoi ces valeurs (statique uniquement)

- Tauri ne supporte pas les solutions serveur (SSR) : export statique obligatoire via `output: 'export'`.
- Dossier de sortie `out` → `frontendDist: "../out"` dans `tauri.conf.json`.
- `images.unoptimized: true` car l'optimisation d'images Next.js exige un serveur.
- `devUrl http://localhost:3000` + commandes pnpm `dev` / `build` (onglet pnpm de la doc ; npm/yarn/deno identiques).
- Pas de `assetPrefix` mobile ici (cas desktop) ; la doc prévoit `assetPrefix: http://${internalHost}:3000` uniquement pour joindre le dev-server sur IP interne en mobile.

## Sources

- `tauri-docs` commit `ec113a50`, EN canonique seule — fichier `src/content/docs/start/frontend/nextjs.mdx` (titre `Next.js`, Next.js 14.2.3) : checklist `output: 'export'` + `frontendDist` = dossier `out`.
- Skill `tauri-start` : `SKILL.md` (routage frontends meta), `references/frontend-meta.md` § Next.js, `examples/tauri.conf.nextjs.json`.

## Validation

```
OK .../with_skill/outputs/tauri.conf.json: frontend=nextjs, frontendDist=../out, devUrl=http://localhost:3000
```

Commande : `python3 skills/tauri-start/scripts/check-start.py .../with_skill/outputs/tauri.conf.json --frontend nextjs` → code retour 0.
