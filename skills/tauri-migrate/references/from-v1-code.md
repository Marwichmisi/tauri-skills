# Migration v1 : code Rust / JS / mobile — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/start/migrate/from-tauri-1.mdx` (titre `Upgrade from Tauri 1.0`, § Preparing for Mobile, Automated Migration, Rust Crate Changes, JavaScript API Changes, Event System, Multiwebview, New origin URL, Detailed Migration Steps)
- `tauri-docs/src/content/docs/start/migrate/index.mdx` (titre `Upgrade & Migrate`, vue d'ensemble)

## Vue d'ensemble (index.mdx)

> Learn about common scenarios and steps to upgrade from Tauri 1.0 or migrate from another framework.

Deux cartes : `Upgrade from Tauri 1.0` (updates pour passer un projet v1 en v2) et `Migrate from Tauri 2.0 beta` (updates bêta 2.0 → 2.0). Router ci-dessous vers la bonne référence.

## Commande `migrate` (même fichier)

> The Tauri v2 CLI includes a `migrate` command that automates most of the process and helps you finish the migration.

:::danger
This command is not a substitute for this guide! Please read the _whole_ page regardless of whether you chose to use the command.
:::

Voir `examples/migrate-commands.sh` (npm/yarn/pnpm/cargo, onglets doc). Référence CLI : skill frère `tauri-config-cli-reference` (`reference/_cli.mdx`, section `migrate`).

## Mobile : crate lib (même fichier, § Preparing for Mobile)

> The mobile interface of Tauri requires your project to output a shared library.

1. `[lib] name = "app_lib"`, `crate-type = ["staticlib", "cdylib", "rlib"]` dans `Cargo.toml`.
2. `src-tauri/src/main.rs` → `src-tauri/src/lib.rs`.
3. `pub fn run()` avec `#[cfg_attr(mobile, tauri::mobile_entry_point)]` dans `lib.rs`.
4. Recréer `main.rs` appelant `app_lib::run()`.

Voir `examples/Cargo.v2-mobile.toml`. Vérifié par `scripts/check-migrate.py --cargo-toml --mobile`.

## Cargo features (même fichier, listes exactes)

Nouvelles : `linux-protocol-body` (custom protocol request body, webkit2gtk 2.40).
Supprimées : `reqwest-client` (reqwest seul supporté), `reqwest-native-tls-vendored` (→ `native-tls-vendored`), `process-command-api` (→ plugin `shell`), `shell-open-api` (→ plugin `shell`), `windows7-compat` (→ plugin `notification`), `updater` (→ plugin), `linux-protocol-headers` (défaut, webkit2gtk minimum relevé), `system-tray` (renommé `tray-icon`).

## Rust / JS : règle de remplacement (même fichier)

- `api` module removed. Each API module can be found in a Tauri plugin.
- `@tauri-apps/api/tauri` → `@tauri-apps/api/core` ([Migrate to Core Module](#migrate-to-core-module)).
- `@tauri-apps/api/window` → `@tauri-apps/api/webviewWindow` ; Rust `Window` → `WebviewWindow`, `WindowBuilder` → `WebviewWindowBuilder`, `WindowUrl` → `WebviewUrl`, `get_window` → `get_webview_window` ([Migrate to new Window API](#migrate-to-new-window-api)).
- Modules JS `cli/clipboard/dialog/fs/global-shortcut/http/notification/os/process/shell/updater` → `@tauri-apps/plugin-<nom>` (`^2.0.0`, voir table ci-dessous pour le nom exact) + `tauri-plugin-<nom> = "2"` côté Cargo avec `.plugin(...)` dans le Builder. Détail par plugin dans le même fichier : voir table de routage (Menu, Tray, Path, Shell, Updater…).
- Cas particulier documenté (même fichier, § Migrate to Clipboard Plugin) : côté JS le paquet est `@tauri-apps/plugin-clipboard-manager` (`import { writeText } from '@tauri-apps/plugin-clipboard-manager'`), côté Rust la crate est `tauri_plugin_clipboard` (`use tauri_plugin_clipboard::{ClipboardExt, ClipKind}`). Les deux noms coexistent dans la doc, ne pas les uniformiser.
- Rust `tauri::api::dialog/file/http`, `api::process::Command`, `tauri::api::shell`, `Manager::shell_scope`, `Manager::fs_scope` (→ `tauri_plugin_fs::FsExt`), `App::clipboard_manager`, `App::get_cli_matches`, `App::global_shortcut_manager`, `Menu*/SystemTray*` (→ `tauri::menu::*` via muda, `tauri::tray::TrayIconBuilder`), `updater`, `api::path` (→ `tauri::Manager::path`), `api::version` (→ crate `semver`), `Env.args` (→ `Env.args_os`).
- `v1Compatible` rappelé pour l'updater si app déjà distribuée (voir `from-v1-config.md`).
- Les plugins v1 étaient publiés via git `tauri-plugin-<plugin>-api` ; en v2 ils sont publiés `@tauri-apps/plugin-<plugin-name>`.

Voir `examples/main.v1.js` (avant, KO) et `examples/main.v2.js` (après, OK).

## Events / multiwebview / URL Windows (même fichier, résumé fidèle)

- `emit` émet vers tous les listeners ; nouveau `emit_to`/`emitTo` vers une cible ; `emit_filter` filtre sur [`EventTarget`](https://docs.rs/tauri/2.0.0/tauri/event/enum.EventTarget.html) ; `listen_global` renommé `listen_any` ; JS `event.listen()` ≈ `listen_any` sauf `Options.target` ; `WebviewWindow.listen` n'écoute que sa cible.
- Multiwebview derrière feature `unstable` : Rust `Window` → `WebviewWindow` (voir ci-dessus).
- Windows : frontend servi sur `http://tauri.localhost` (au lieu de `https`) ; IndexedDB/LocalStorage/Cookies réinitialisés sauf `app > windows > useHttpsScheme: true` (ou `WebviewWindowBuilder::use_https_scheme`) pour garder `https`.

## Permissions (même fichier, § Migrate Permissions)

> The v1 allowlist have been rewritten to a completely new system for permissions […] you must create capability files inside the `src-tauri/capabilities` folder […] The `migrate` CLI command automatically parses your v1 allowlist and generates the associated capability file. To learn more […] see [the security documentation](/security/).

Doctrine complète : skill frère `tauri-security-capabilities`. Ici on ne fait que nommer le dossier `capabilities/` et la commande `migrate`.
