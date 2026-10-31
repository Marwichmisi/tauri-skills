# Transcript — eval titlebar (with_skill)

1. Lu `SKILL.md` (routage titlebar → `references/windows.md`, `examples/titlebar.js`, `examples/tauri.conf.windows.json`, check `--frontend` + `--config`).
2. Lu `references/windows.md` (source `learn/window-customization.mdx`, commit `ec113a50`), `examples/titlebar.js`, `examples/tauri.conf.windows.json`.
3. Vérifié le doc canonique `tauri-docs/src/content/docs/learn/window-customization.mdx` (extraits `decorations: false`, capability 5 permissions, `data-tauri-drag-region`, `app-region: drag`, `getCurrentWindow` + `minimize`/`toggleMaximize`/`close`, variante `startDragging`).
4. Produit `outputs/tauri.conf.json` (`app.windows[0]` : `label: main` + `decorations: false`) et `outputs/titlebar.js` (copie fidèle de l'exemple/doc).
5. Lançé `python3 skills/tauri-ui-recettes/scripts/check-ui-recettes.py --config <tauri.conf.json> --frontend <titlebar.js>` → `OK` config (`windows: ['main']`) + `OK` frontend (`getCurrentWindow`), sans permission inventée.
6. Écrit `answer.md` (sources + commandes + sortie OK) et ce `transcript.md`.
