---
name: tauri-ui-recettes
description: Build idiomatic Tauri v2 native UI (custom windows/titlebar, menus, tray, splashscreen, mobile multiwindow, file associations). Use me whenever the agent creates windows, menus, tray icons, splashscreens, mobile windows or file associations — I own the UI-recipes doctrine, permission doctrine lives in tauri-security-capabilities and sidecar/updater/config-schema go to brothers.
---

# Tauri UI Recettes

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust / Kotlin / Swift linkées, jamais copiées.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (fenêtre vs menu vs tray vs splashscreen vs mobile).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-ui-recettes.py` avec le mode du tableau pour valider tout artefact.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Custom titlebar / decorations / drag-region / transparent macOS | `references/windows.md` | `examples/titlebar.js`, `examples/tauri.conf.windows.json` | `scripts/check-ui-recettes.py --frontend` + `--config` |
| Menu fenêtre natif (base, multi-niveaux, prédéfini, events, anti-leak) | `references/menus.md` | `examples/menu.js` | `scripts/check-ui-recettes.py --frontend` |
| Tray (Cargo `tray-icon`, icône, menu, `menuOnLeftClick`, events Click/DoubleClick) | `references/tray.md` | `examples/tray.js` | `scripts/check-ui-recettes.py --frontend` |
| Splashscreen (main hidden + splashscreen, setup front/back, close/show) | `references/splashscreen.md` | `examples/tauri.conf.windows.json`, `examples/splashscreen.rs` | `scripts/check-ui-recettes.py --config` + `--rust` |
| Mobile multi-fenêtres (capability `allow-create-webview-window`, Android embedding, iOS scenes, WebviewWindow) | `references/mobile.md` | `examples/mobile-windows.js`, `examples/mobile-windows.rs` | `scripts/check-ui-recettes.py --frontend` + `--rust` |
| Associations fichiers mobile (`bundle.fileAssociations`, `RunEvent::Opened` cold+warm) | `references/mobile.md` | `examples/tauri.conf.file-associations.json`, `examples/mobile-windows.js`, `examples/mobile-windows.rs` | `scripts/check-ui-recettes.py --config` + `--frontend` + `--rust` |
| Doute inter-skill (permission/capability, sidecar Node, updater, schéma complet) | voir Frontières | — | — |

## Frontières

- `tauri-security-capabilities` : seule autorité capabilities/permissions/scopes (`core:window:*`, `core:webview:allow-create-webview-window`, CSP/asset-protocol). Ici on cite les permissions doc sans inventer, doctrine là-bas.
- `tauri-ipc-bridge` : sidecar Node (`learn/sidecar-nodejs.mdx` vit là-bas), commands/events/state/resources. Ici `invoke`/`emit`/`listen` seulement comme patterns splashscreen/file-open.
- `tauri-distribution` : updater, installateurs, stores, signing, pipelines. Ici aucune cible bundle ni var de signature.
- `tauri-config-cli-reference` : schéma complet `tauri.conf.json`/`gen/schemas`, CLI, env-vars, webviews. Ici fenêtres `app.windows` + `bundle.fileAssociations` seuls.
- `tauri-start`, `tauri-migrate`, `tauri-core-concepts`, `tauri-dev-quality`, `tauri-plugin-dev`, `tauri-plugins-catalogue`, `tauri-frontend-bindings` : hors périmètre UI-recettes ; renvoyer si le besoin réel y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule). `learn/index.mdx` = routeur sans doctrine.

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucun contenu inventé. Labels uniques, `visible`/`decorations` booléens, splashscreen exige `main` hidden ; `ext` sans point, `role`/`rank`/`androidIntentActionFilters` enums doc seules ; JS `TrayIcon.new`/`Menu.new` + `await using`/`close`, Rust `TrayIconBuilder`/`WebviewWindowBuilder`/`RunEvent::Opened` + `emit("opened")` / `SceneRequested` + builder.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Titlebar : `examples/titlebar.js`. Menu : `examples/menu.js`. Tray : `examples/tray.js`.
Splashscreen : `examples/tauri.conf.windows.json` + `examples/splashscreen.rs`.
Mobile : `examples/mobile-windows.js` + `examples/mobile-windows.rs` + `examples/tauri.conf.file-associations.json`.
Valider avec `python3 scripts/check-ui-recettes.py --config examples/tauri.conf.windows.json`, `--config examples/tauri.conf.file-associations.json`, `--frontend examples/menu.js`, `--frontend examples/tray.js`, `--rust examples/splashscreen.rs`.
