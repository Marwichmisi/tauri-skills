# Transcript — eval-sveltekit-spa (with_skill)

Skill : `/media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start` (`SKILL.md`)
Commit doc : `ec113a50`, EN canonique seule.

## Lectures

1. `SKILL.md` — routage : Configurer Next/Nuxt/SvelteKit/Qwik → `references/frontend-meta.md`, exemples `tauri.conf.*.json`, script `scripts/check-start.py --frontend sveltekit`.
2. `references/frontend-meta.md` § SvelteKit — checklist SSG+SPA via static-adapter, SPA sans prerender, `frontendDist build/`, bloc Tauri pnpm (`pnpm dev` / `pnpm build` / `:5173` / `../build`), `npm install --save-dev @sveltejs/adapter-static`, `adapter({ fallback: 'index.html' })`, `src/routes/+layout.ts` avec `export const ssr = false;`.
3. `examples/tauri.conf.sveltekit.json` — bloc build recopié tel quel vers `outputs/tauri.conf.json`.
4. `references/project-structure.md` + `examples/project-structure.txt` — arbre attendu, 5 fichiers requis pour `--project-root`.
5. `references/create-project.md`, `references/frontend-vite.md`, `scripts/check-start.py` — règle pas de SSR / hôte statique, usage du check.

## Écriture

- `outputs/tauri.conf.json` : copie exacte de l'exemple sveltekit.

## Check exécuté

```sh
python3 /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start/scripts/check-start.py /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start-workspace/iteration-1/eval-sveltekit-spa/with_skill/outputs/tauri.conf.json --frontend sveltekit
```

Résultat :

```
OK /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start-workspace/iteration-1/eval-sveltekit-spa/with_skill/outputs/tauri.conf.json: frontend=sveltekit, frontendDist=../build, devUrl=http://localhost:5173
```

Check structure documenté (non exécuté ici, exige un vrai projet) :

```sh
python3 scripts/check-start.py src-tauri/tauri.conf.json --project-root .
```

## Frontière déclarée

Schéma complet → `tauri-config-cli-reference`. Réponse limitée au bloc `build` + `ssr:false` / adapter-static.
