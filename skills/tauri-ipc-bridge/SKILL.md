---
name: tauri-ipc-bridge
description: Make Rust and frontend talk in Tauri v2 (commands/invoke, events/listen/emit, channels, state, resources, sidecars incl. Node, config files, icons). Use me whenever the agent writes a command, listens/emits, manages state, bundles resources/sidecars, or touches develop/* — I own the IPC bridge doctrine, scopes/permissions go to tauri-security-capabilities, full config schema to tauri-config-cli-reference.
---

# Tauri IPC Bridge

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée.
> Gabarit valable pour les 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (command vs event vs state vs resource vs sidecar vs config/icone).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-ipc-bridge.py` pour valider tout echange Rust<->frontend et toute config `bundle`.
5. Renvoyer vers les skills freres si hors perimetre (voir Frontieres).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Exposer/appeler une commande Rust (`#[tauri::command]`, args camelCase, retour, erreur, async) | `references/commands.md` | `examples/command-rust.rs` + `examples/command-frontend.js` | `scripts/check-ipc-bridge.py --rust ... --frontend ...` |
| Emettre/ecouter (event global/webview, `listen`/`emit`, `once`/`unlisten`, channels, `eval`) | `references/events.md` | `examples/event-rust.rs` + `examples/event-frontend.js` | `scripts/check-ipc-bridge.py --rust ... --frontend ...` |
| Gerer l'etat (`manage`, `Mutex`, `State`, `Manager`) | `references/state.md` | `examples/state.rs` | — (renvoi doc, check via paire command) |
| Embarquer des fichiers (`bundle.resources`, `resolve`, Android) | `references/resources.md` | `examples/tauri.conf.resources.json` | `scripts/check-ipc-bridge.py --config ...` |
| Embarquer un binaire (`externalBin`, `-triple`, `shell().sidecar`, `Command.sidecar`, args) + doublon Node (`pkg`) | `references/sidecar.md` | `examples/tauri.conf.sidecar.json` + `examples/sidecar-rename.js` | `scripts/check-ipc-bridge.py --config ... [--rust ... --frontend ...]` |
| Fichiers/dev/icones (`tauri.conf.json`, `Cargo.toml`, `package.json`, `tauri dev`, `tauri icon`, `bundle.icon`) | `references/app-config.md` | `examples/tauri.conf.dev.json` + `examples/bundle-icon.json` | `scripts/check-ipc-bridge.py --config ...` (bundle seul) |
| Doute inter-skill (permission/scope, schema complet, fiche plugin) | voir Frontieres | — | — |

## Frontieres

- `tauri-security-capabilities` : seule autorite sur capabilities, permissions, scopes (`shell:allow-execute/spawn`, `fs:allow-*`, `$RESOURCE/**`), CSP, asset-protocol, headers, lifecycle. Ici on ne declare aucune permission ; tout `plugin:…`, `capability`, `scope`, `allow/deny` remonte la-bas.
- `tauri-config-cli-reference` : schema complet `tauri.conf.json`/`gen/schemas`, env-vars, webviews, CLI (`tauri dev/build/icon/init`). Ici on ne montre que les snippets `build`/`bundle` documentes par `develop/*`.
- `tauri-plugins-catalogue` : fiches `plugin/*` (shell, fs, opener). Ici on cite `Command.sidecar`/`resolveResource` sans dupliquer la doctrine.
- `tauri-core-concepts` : conception (events vs commands, brownfield/isolation, taille). Ici implementation cote code.
- `tauri-start` / `tauri-migrate` : scaffolding et migration. Ici projet existant.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Regle anti-drift

- Extraits `references/` = copies fideles de `tauri-docs/` avec pointeur `Source:` en tete (fichier + commit + titre frontmatter).
- Aucun contenu invente. Noms de commandes uniques, `pub` interdit dans `lib.rs`, args camelCase (ou `rename_all`), `invoke_handler` unique, sidecar `-$TARGET_TRIPLE` sur disque mais jamais dans `externalBin`, `Command.sidecar` == entree `externalBin`, Rust `sidecar()` == basename.
- `SKILL.md` < 500 lignes ; le detail vit en `references/`, jamais ici.

## Exemple minimal

Echange complet (command) : `examples/command-rust.rs` + `examples/command-frontend.js`.
Events : `examples/event-rust.rs` + `examples/event-frontend.js`.
Etat : `examples/state.rs` (via `State`, verifie par la paire command).
Valider avec `python3 scripts/check-ipc-bridge.py --rust examples/command-rust.rs --frontend examples/command-frontend.js` et `--config examples/tauri.conf.sidecar.json`.
