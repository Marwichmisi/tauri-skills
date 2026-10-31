---
name: tauri-plugin-dev
description: Author a Tauri v2 plugin for desktop and mobile with valid identifiers, permissions, platform support and guest bindings. Use me whenever the agent scaffolds a plugin, writes permissions/scopes/sets/default/build.rs, declares platform support, wires Builder/lifecycle/invoke, or adds Android Kotlin/iOS Swift commands — I own the plugin-dev doctrine, permission doctrine lives in tauri-security-capabilities and IPC code in tauri-ipc-bridge.
---

# Tauri Plugin Dev

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust / Kotlin / Swift linkées, jamais copiées.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (scaffold desktop vs permission/scope vs support/config/lifecycle vs mobile).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-plugin-dev.py` avec le mode du tableau pour valider tout artefact.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Nommer/scaffolder (`plugin new`, `--no-api/--android/--ios`, `tauri-plugin-[name]/`, `Builder`, lifecycle, `invoke_handler`, `guest-js`) | `references/plugin-basics.md` | `examples/Cargo.plugin.toml`, `examples/lib-plugin.rs`, `examples/commands-upload.rs`, `examples/guest-js-upload.js`, `examples/tauri-conf-plugin.json` | `scripts/check-plugin-dev.py --identifier <nom>` + `--invoke <js/rs>` |
| Écrire permissions (`allow/deny`, `scope`, `set`, `default`, `build.rs` autogen) | `references/permissions.md` | `examples/permission-allow-start-server.toml`, `examples/permission-scope-spawn-node.toml`, `examples/permission-set-websocket.toml`, `examples/permission-default.toml`, `examples/build-rs-autogen.rs` | `scripts/check-plugin-dev.py --permission <toml>` |
| Déclarer support plateformes (`windows/linux/macos/android/ios`, `full/partial/none`) | `references/plugin-basics.md` | `examples/Cargo.plugin.toml` | `scripts/check-plugin-dev.py --cargo <toml>` |
| Ajouter mobile (Kotlin `@Command`, Swift `@objc`, `run_mobile_plugin`, args, JNI/FFI, 16KB, `checkPermissions`, `trigger`/`addPluginListener`) | `references/mobile.md` | `examples/mobile-command.kt`, `examples/mobile-command.swift`, `examples/mobile-invoke.rs`, `examples/plugin-listener.js` | `scripts/check-plugin-dev.py --invoke <kt/swift/rs/js>` |
| Doute inter-skill (capability côté app, scope côté code, fiche catalogue) | voir Frontières | — | — |

## Frontières

- `tauri-security-capabilities` : seule autorité capabilities/permissions côté app (`capabilities/*.json`, `plugin:scope:cle`, `deny` > `allow`, CSP/asset-protocol). Ici côté auteur (`permissions/*.toml`, `build.rs`, `trigger` exige `<plugin>:default` en capability, doctrine vit là-bas).
- `tauri-ipc-bridge` : implémentation commands/events/state/resources/sidecar côté app (`#[tauri::command]`, `invoke_handler` app, `Channel`, `State`, `AppManifest::commands`). Ici côté plugin (`commands.rs` exposée via `Builder`, `desktop.rs`/`mobile.rs`, `scope.rs` + `CommandScope`/`GlobalScope` lus ici, détail IPC là-bas).
- `tauri-plugins-catalogue` : les 30 fiches `plugin/*` (usage). Ici auteur (création), la fiche vit là-bas.
- `tauri-config-cli-reference` : schéma complet `tauri.conf.json`/`gen/schemas`, CLI (`plugin new/android/ios`), env-vars. Ici on ne montre que `plugins.<nom>` + `platforms.support`.
- `tauri-start`, `tauri-migrate`, `tauri-core-concepts`, `tauri-dev-quality`, `tauri-distribution`, `tauri-ui-recettes`, `tauri-frontend-bindings` : hors périmètre plugin-dev ; renvoyer si le besoin réel y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucun contenu inventé. Identifiants doc seuls (`sqlite`, `sqlite-store`, `allow-start-server`, `my-plugin:default`), commandes snake_case (`upload`, `start_server`, `spawn`), mobile `openCamera`/`checkPermissions`/`requestPermissions`, `invoke('plugin:<nom>|<cmd>')`, `Builder::new("<nom>")`, `run_mobile_plugin("openCamera")`, `addPluginListener('<nom>', '<event>')`, plateformes `windows/linux/macos/android/ios` + `full/partial/none` seuls.
- Desktop `mobile.rs` vs mobile `init` : citer la forme du fichier lu (`add` côté `index.mdx`, `init` côté `develop-mobile.mdx`), ne jamais fusionner.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Squelette desktop : `examples/lib-plugin.rs` + `examples/commands-upload.rs` + `examples/guest-js-upload.js` + `examples/Cargo.plugin.toml` + `examples/permission-allow-start-server.toml`.
Valider avec `python3 scripts/check-plugin-dev.py --identifier my-plugin`, `--permission examples/permission-allow-start-server.toml`, `--cargo examples/Cargo.plugin.toml`, `--invoke examples/guest-js-upload.js`.
Mobile : `examples/mobile-command.kt` + `examples/mobile-command.swift` + `examples/mobile-invoke.rs` + `examples/plugin-listener.js`.
Valider avec `python3 scripts/check-plugin-dev.py --invoke examples/mobile-invoke.rs` et `--invoke examples/plugin-listener.js`.
