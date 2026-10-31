# Scaffold plugin desktop `my-plugin` — conforme doc (avec skill)

## Sources (pointeurs exigés)
- Fichier : `tauri-docs/src/content/docs/develop/Plugins/index.mdx`
- Commit : `ec113a50`
- Titre (frontmatter) : `Plugin Development`
- Skill appliqué : `skills/tauri-plugin-dev` → `references/plugin-basics.md` → `examples/Cargo.plugin.toml`, `examples/lib-plugin.rs`, `examples/commands-upload.rs`, `examples/guest-js-upload.js`, `examples/tauri-conf-plugin.json` → `scripts/check-plugin-dev.py --identifier/--cargo/--invoke`

> Extraits doc : copies fidèles via `references/plugin-basics.md`. API Rust/Kotlin/Swift linkées (`docs.rs`), jamais copiées. Aucun identifiant inventé : seuls `my-plugin`, `upload`, plateformes `windows/linux/macos/android/ios` + `full/partial/none`.

## 1. Nommage + arborescence
- Crate : `tauri-plugin-my-plugin` (règle doc : `By default Tauri prefixes your plugin crate with tauri-plugin-` ; crate `tauri-plugin-{plugin-name}`).
- Bootstrap : `npx @tauri-apps/cli plugin new my-plugin` (`plugin new` ; `--no-api` si pas de NPM ; `--android`/`--ios` pour mobile — non utilisés ici, scaffold desktop).
- Arborescence doc (index.mdx) :
  - `tauri-plugin-my-plugin/src/commands.rs` — `Defines the commands the webview can use`
  - `src/desktop.rs` — `Desktop implementation`
  - `src/mobile.rs` — `Mobile implementation`
  - `src/lib.rs` — `Re-exports appropriate implementation, setup state...`
  - `guest-js/` + `Cargo.toml` + `tauri.conf.json` (`plugins.my-plugin`)
- Identifier `my-plugin` valide : lowercase ASCII + tiret non leading/trailing (tableau Identifier Rules : `sqlite` oui, `sqlite-store` oui, `sqlite_store` non, `-sqlite` non).

## 2. `src/commands.rs` — commande `upload` (snake_case, `Channel`)
Copie fidèle de `examples/commands-upload.rs` (lui-même extrait `src/commands.rs` de index.mdx) :

```rust
use tauri::{command, ipc::Channel, AppHandle, Runtime, Window};

#[command]
async fn upload<R: Runtime>(app: AppHandle<R>, window: Window<R>, on_progress: Channel, url: String) {
    // implement command logic here
    on_progress.send(100).unwrap();
}
```

Doc : `Commande (src/commands.rs, AppHandle/Window par injection, Channel, args comme une commande app)`. Détail IPC (`Channel`, `State`) : voir skill frère `tauri-ipc-bridge`.

## 3. `src/lib.rs` — `Builder::new("my-plugin")` + `invoke_handler` + `setup`
Copie fidèle de `examples/lib-plugin.rs` (extrait `src/lib.rs` Builder/config + enregistrement handler de index.mdx) :

```rust
use tauri::plugin::Builder;

pub fn init<R: tauri::Runtime>() -> tauri::plugin::TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![crate::commands::upload])
        .setup(|app, api| {
            // Register state, spawn background tasks here (setup lifecycle).
            // Mobile plugins are registered here in generated template.
            Ok(())
        })
        .build()
}
```

Appariement exigé : `Builder::new("my-plugin")` + `.invoke_handler(tauri::generate_handler![crate::commands::upload])` + `setup` (lifecycle : `setup: Plugin is being initialized — Register mobile plugins, manage state, run background tasks`). Config `timeout` parsée au runtime via `Builder::<R, Config>::new("<plugin-name>")` + `api.config().timeout` (voir §5).

## 4. `src/desktop.rs` / `src/mobile.rs`
Doc : `The plugin APIs defined in the project's desktop.rs and mobile.rs are exported to the user as a struct with the same name as the plugin (in pascal case) [...] through the extension trait defined in the plugin.`

```rust
// desktop.rs
pub struct MyPlugin<R: tauri::Runtime>(std::marker::PhantomData<R>);
impl<R: tauri::Runtime> MyPlugin<R> {
    pub fn upload(&self, _url: String) { /* desktop impl of `upload` */ }
}
```

`mobile.rs` : stub fallback desktop-first (même struct) ; ajout mobile réel via `plugin android add` / `plugin ios add` (wording index.mdx ; le guide mobile dit `plugin android init` / `plugin ios init` — les deux formes citées telles quelles). Mobile (`openCamera`, `run_mobile_plugin`, `addPluginListener`) : hors périmètre de ce scaffold, voir `references/mobile.md`.

## 5. `guest-js` — `invoke('plugin:my-plugin|upload')` avec `Channel`
Copie fidèle de `examples/guest-js-upload.js` (extrait `webview-src/index.ts` de index.mdx) :

```js
import { invoke, Channel } from '@tauri-apps/api/core'

export async function upload(url: string, onProgressHandler: (progress: number) => void): Promise<void> {
  const onProgress = new Channel<number>()
  onProgress.onmessage = onProgressHandler
  await invoke('plugin:my-plugin|upload', { url, onProgress })
}
```

Règle : `invoke('plugin:<plugin-name>|upload')`, build TS avant test.

## 6. `Cargo.toml` — `platforms.support`
Copie fidèle de `examples/Cargo.plugin.toml` (bloc `Cargo.toml` de index.mdx) :

```toml
[package]
name = "tauri-plugin-my-plugin"
version = "0.1.0"

[package.metadata.platforms.support]
windows = { level = "full" }
linux = { level = "full" }
macos = { level = "full" }
android = { level = "partial", notes = "Access is restricted to the Application folder by default" }
ios = { level = "none" }
```

Règle : chaque clé = plateforme (`windows`, `linux`, `macos`, `android`, `ios`), `level` requis (`full`/`partial`/`none`), `notes` Markdown optionnel.

## 7. `tauri.conf.json` — `plugins.my-plugin.timeout = 30`
Copie fidèle de `examples/tauri-conf-plugin.json` (bloc Plugin Configuration côté app, clé `plugins.<plugin-name>`) :

```json
{
  "build": {},
  "tauri": {},
  "plugins": {
    "my-plugin": {
      "timeout": 30
    }
  }
}
```

Schéma complet : voir skill frère `tauri-config-cli-reference` ; ici seuls `plugins.<nom>` + `platforms.support`.

## 8. Validation `scripts/check-plugin-dev.py` — tout OK
```
$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --identifier my-plugin
OK identifier 'my-plugin' valide (develop/Plugins/index.mdx)

$ python3 scripts/check-plugin-dev.py --cargo <outputs>/Cargo.plugin.toml
OK <outputs>/Cargo.plugin.toml: platforms.support fidèle (windows=full, linux=full, macos=full, android=partial, ios=none)

$ python3 scripts/check-plugin-dev.py --invoke <outputs>/guest-js-upload.js
OK <outputs>/guest-js-upload.js: invoke plugin fidèle
 - invoke plugin:my-plugin|upload

$ python3 scripts/check-plugin-dev.py --invoke <outputs>/lib.rs
OK <outputs>/lib.rs: invoke plugin fidèle
 - Builder::new("my-plugin")
```
Tous `rc=0`. (`src/commands.rs` seul n'est pas passé à `--invoke` : sans `Builder::new` il est rejeté par design — `commande Rust sans Builder::new ni invoke_handler` — c'est `lib.rs` qui l'enregistre.)

## Frontières (rappel doctrine)
- Capabilities/permissions côté app (`capabilities/*.json`, `deny` > `allow`) : autorité `tauri-security-capabilities`.
- Implémentation IPC côté app (`#[tauri::command]`, `Channel`, `State`) : détail `tauri-ipc-bridge`.
- Fiches usage des 30 plugins : `tauri-plugins-catalogue`. Schéma `tauri.conf` complet / CLI : `tauri-config-cli-reference`.
