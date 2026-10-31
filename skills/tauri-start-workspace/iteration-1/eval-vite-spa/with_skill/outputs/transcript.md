# Transcript — eval-vite-spa (with_skill)

## Fichiers lus (skill tauri-start)

1. `skills/tauri-start/SKILL.md` — workflow, tableau de routage (Vite → `references/frontend-vite.md` + `examples/tauri.conf.vite.json` + `check-start.py --frontend vite`), règle anti-drift (seuls `frontendDist`/`devUrl` documentés, commit `ec113a50`, EN canonique).
2. `skills/tauri-start/references/frontend-vite.md` — checklist frontend (hôte statique, SSG/SPA/MPA, pas de SSR, serveur dev sur IP interne pour mobile), checklist Vite (`../dist`, `TAURI_DEV_HOST`), bloc `build` pnpm, rappel `vite.config` (`clearScreen`, `port`/`strictPort`, `host`/`hmr`, `watch.ignored`, `envPrefix`, `build.target`).
3. `skills/tauri-start/references/project-structure.md` — arbre `src-tauri/` + rôles (`tauri.conf.json`, `capabilities/`, `icons/`, `build.rs`, `lib.rs`, `main.rs`), principe hôte statique.
4. `skills/tauri-start/references/prerequisites.md` — système (Linux/macOS/Windows), Rust, Node, mobile (Android/iOS).
5. `skills/tauri-start/references/create-project.md` — `create-tauri-app` + setup manuel (`pnpm create vite .`, `tauri init`, ignore `src-tauri` côté watcher).
6. `skills/tauri-start/examples/tauri.conf.vite.json` — bloc `build` pnpm copié tel quel vers outputs.
7. `skills/tauri-start/examples/vite.config.example.js` — config Vite copiée telle quelle en rappel.
8. `skills/tauri-start/examples/project-structure.txt` — arbre copié tel quel.
9. `skills/tauri-start/scripts/check-start.py` — règles de validation lues avant exécution.

## Commande check lancée

```
python3 /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start/scripts/check-start.py /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start-workspace/iteration-1/eval-vite-spa/with_skill/outputs/tauri.conf.json --frontend vite
```

Résultat :
```
OK /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-start-workspace/iteration-1/eval-vite-spa/with_skill/outputs/tauri.conf.json: frontend=vite, frontendDist=../dist, devUrl=http://localhost:5173
```

Exit 0. Aucune valeur inventée.
