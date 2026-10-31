# Transcript

## Fichiers lus

1. `skills/tauri-start/SKILL.md` — workflow + tableau de routage (ligne Next/Nuxt/SvelteKit/Qwik → `references/frontend-meta.md` + `examples/tauri.conf.nextjs.json` + `check-start.py --frontend nextjs`).
2. `skills/tauri-start/references/frontend-meta.md` — § Next.js : `output: 'export'`, `frontendDist ../out`, `devUrl http://localhost:3000`, `beforeDev pnpm dev` / `beforeBuild pnpm build`, `next.config.mjs` avec `output: 'export'` + `images.unoptimized` (+ `assetPrefix` mobile seul).
3. `skills/tauri-start/examples/tauri.conf.nextjs.json` — bloc `build` repris tel quel.
4. `skills/tauri-start/scripts/check-start.py` — règles `nextjs: frontendDist ../out, devPort 3000`.

## Commande check

```
python3 /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start/scripts/check-start.py /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start-workspace/iteration-1/eval-nextjs-export/with_skill/outputs/tauri.conf.json --frontend nextjs
```

Résultat :

```
OK .../with_skill/outputs/tauri.conf.json: frontend=nextjs, frontendDist=../out, devUrl=http://localhost:3000
```

Code retour : 0 (PASS).
