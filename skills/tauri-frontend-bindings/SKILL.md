---
name: tauri-frontend-bindings
description: Call the right Tauri v2 JS/TS frontend API (core invoke/Channel/event, app/path/window, 27 plugin guest-js) with Rust docs.rs links only. Use me whenever the agent writes frontend JS/TS calling Tauri, picks a core vs plugin module, mocks Tauri APIs, or needs convertFileSrc/Channel/Resource — I own the JS-bindings doctrine, IPC Rust code lives in tauri-ipc-bridge, permissions in tauri-security-capabilities, config schema in tauri-config-cli-reference.
---

# Tauri Frontend Bindings

> Source-de-vérité : `tauri-docs/` commit `ec113a50` (EN canonique seule) +
> régénéré JS avant écriture : `tauri@37b3be6 packages/api/src`,
> `plugins-workspace@df59420 plugins/*/guest-js` (27 modules).
> Ne cite rien hors ces sources. Traductions ignorées. API Rust linkée (`docs.rs`), jamais copiée.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (core vs event vs app/path/window vs plugin vs mocks).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-frontend-bindings.py` pour valider imports + signatures.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Appeler Rust (`invoke`, args, headers) / stream (`Channel` + `onmessage`) / asset (`convertFileSrc`) / `Resource` + `await using` / mocks | `references/core-api.md` | `examples/invoke-channel.js` + `examples/channel-rust.rs` + `examples/mocks.js` | `scripts/check-frontend-bindings.py --frontend ... [--rust ...]` |
| Event frontend (`listen`/`once`/`emit`/`emitTo`, `TauriEvent`, `EventTarget`, cleanup `unlisten`) | `references/event-api.md` | `examples/event-listen.js` | `scripts/check-frontend-bindings.py --frontend ...` |
| App/path/window courants (`getVersion`, `BaseDirectory`/`join`, `getCurrentWindow`, `withGlobalTauri`) | `references/app-path-window.md` | `examples/invoke-channel.js` (convert) | `scripts/check-frontend-bindings.py --frontend ...` |
| Plugin guest-js (27 imports `@tauri-apps/plugin-*`, fonction phare) | `references/plugin-apis.md` | `examples/plugin-dialog-fs.js` | `scripts/check-frontend-bindings.py --frontend ...` |
| Doute inter-skill (command Rust, permission/scope, config schéma, fiche plugin) | voir Frontières | — | — |

## Frontières

- `tauri-ipc-bridge` : implémentation Rust ↔ frontend (commands, `generate_handler`, `emit` Rust, `State`, `resources`, sidecars, `develop/*`). Ici JS seul + pendant Rust minimal `Channel` avec lien `docs.rs` exigé (exemple `channel-rust.rs`) ; implémentation complète là-bas.
- `tauri-security-capabilities` : seule autorité capabilities/permissions/scopes (`core:*`, `plugin:*`, `allow/deny`, CSP/asset-protocol). Ici on cite les permissions doc sans inventer, doctrine là-bas.
- `tauri-plugins-catalogue` : 30 fiches `plugin/*` détaillées. Ici tableau 27 imports + fonction phare, détail là-bas.
- `tauri-config-cli-reference` : schéma complet `tauri.conf.json`/`gen/schemas`, ACL, CLI. Ici `withGlobalTauri`/`assetProtocol` cités, schéma là-bas.
- `tauri-ui-recettes` : fenêtres/menus/tray/splashscreen idiomatiques. Ici `getCurrentWindow`/`Menu`/`TrayIcon` signatures seules.
- `tauri-start` / `tauri-migrate` / `tauri-core-concepts` / `tauri-dev-quality` / `tauri-plugin-dev` / `tauri-distribution` : hors périmètre bindings ; renvoyer si besoin réel.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles régénérées avec pointeur `Source:` en tête (tauri `37b3be6`, plugins `df59420`, commit `ec113a50` + lien `docs.rs`).
- Aucun contenu inventé. Imports seuls `@tauri-apps/api/<app|core|dpi|event|image|menu|mocks|path|tray|webview|webviewWindow|window>` et `@tauri-apps/plugin-<27 noms>` ; event `^[A-Za-z0-9_\-/:]+$` ou `tauri://...` ; `Channel` exige `onmessage` ; mocks exigent `api/mocks` ; Rust exige lien `https://docs.rs/tauri`.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Invoke + Channel : `examples/invoke-channel.js` + `examples/channel-rust.rs`.
Events : `examples/event-listen.js`. Plugins : `examples/plugin-dialog-fs.js`.
Mocks : `examples/mocks.js`.
Valider avec `python3 scripts/check-frontend-bindings.py --frontend examples/invoke-channel.js --rust examples/channel-rust.rs`, `--frontend examples/event-listen.js`, `--frontend examples/plugin-dialog-fs.js`.
