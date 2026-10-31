# Plugin desktop — scaffolding, nommage, config, lifecycle, commandes

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Plugins/index.mdx` (titre `Plugin Development`)

> This guide is for developing Tauri plugins. If you're looking for a list of the currently available plugins and how to use them then visit the [Features and Recipes list](/plugin/).

> Plugins are able to hook into the Tauri lifecycle, expose Rust code that relies on the web view APIs, handle commands with Rust, Kotlin or Swift code, and much more.

> A Tauri plugin is composed of a Cargo crate and an optional NPM package that provides API bindings for its commands and events. Additionally, a plugin project can include an Android library project and a Swift package for iOS.

## Nommage (index.mdx)

> By default Tauri prefixes your plugin crate with `tauri-plugin-`. [...] The generated crate name will be `tauri-plugin-{plugin-name}` and the JavaScript NPM package name will be `tauri-plugin-{plugin-name}-api` (although we recommend using an [NPM scope] if possible). The Tauri naming convention for NPM packages is `@scope-name/plugin-{plugin-name}`.

### Identifier Rules (index.mdx, tableau fidèle)

- Lowercase ASCII (`a`-`z`), digits (`0`-`9`), hyphens (`-`).
- Hyphens cannot be first or last.
- Single `:` only with prefix (`<plugin-name>:<permission-name>`).
- No `_`, uppercase, other chars.
- Base ≤64 chars ; with prefix ≤129 chars.

| Exemple doc | Valide ? |
|---|---|
| `sqlite` | oui |
| `sqlite-store` | oui |
| `sqlite-store:allow-read` | oui |
| `sqlite_store` | non (underscore) |
| `SqliteStore` | non (uppercase) |
| `-sqlite` | non (leading hyphen) |
| `sqlite-` | non (trailing hyphen) |
| `sqlite::store` | non (multiple separators) |

> If a plugin or permission identifier violates these rules, the build fails with the error `identifiers can only include lowercase ASCII, hyphens which are not leading or trailing, and a single colon if using a prefix`. The offending value is usually the plugin name in your plugin's `Cargo.toml` or a permission identifier in a `permissions/*.toml` file.

Check : `python3 scripts/check-plugin-dev.py --identifier <nom>`.

## Init projet (index.mdx)

> To bootstrap a new plugin project, run `plugin new`. If you do not need the NPM package, use the `--no-api` CLI flag. If you want to initialize the plugin with Android and/or iOS support, use the `--android` and/or `--ios` flags.

```
npx @tauri-apps/cli plugin new [name]
```

Arborescence générée (index.mdx) : voir `examples/` + squelette doc.

```
. tauri-plugin-[name]/
├── src/                - Rust code
│ ├── commands.rs       - Defines the commands the webview can use
| ├── desktop.rs        - Desktop implementation
| ├── error.rs          - Default error type to use in returned results
│ ├── lib.rs            - Re-exports appropriate implementation, setup state...
│ ├── mobile.rs         - Mobile implementation
│ └── models.rs         - Shared structs
├── permissions/        - This will host (generated) permission files for commands
├── android             - Android library
├── ios                 - Swift package
├── guest-js            - Source code of the JavaScript API bindings
├── dist-js             - Transpiled assets from guest-js
├── Cargo.toml          - Cargo crate metadata
└── package.json        - NPM package metadata
```

> If you have an existing plugin and would like to add Android or iOS capabilities to it, you can use `plugin android add` and `plugin ios add` to bootstrap the mobile library projects and guide you through the changes needed.

Note doc : le guide mobile dit `plugin android init` / `plugin ios init` pour le même besoin (`references/mobile.md`). Les deux formes sont citées telles quelles, ne pas inventer une troisième.

## Platform support (index.mdx)

```toml title="Cargo.toml"
[package.metadata.platforms.support]
windows = { level = "full" }
linux = { level = "full" }
macos = { level = "full" }
android = { level = "partial", notes = "Access is restricted to the Application folder by default" }
ios = { level = "none" }
```

> Each key is a platform (`windows`, `linux`, `macos`, `android`, `ios`) and accepts two fields: `level` (required: `"full"` / `"partial"` / `"none"`), `notes` (optional Markdown).

Voir `examples/Cargo.plugin.toml`. Check : `python3 scripts/check-plugin-dev.py --cargo examples/Cargo.plugin.toml`.

## Plugin Configuration (index.mdx)

Dans l'app consommatrice (`tauri.conf.json`, clé `plugins.<plugin-name>`) :

```json
{
  "build": { "...": "..." },
  "tauri": { "...": "..." },
  "plugins": {
    "plugin-name": {
      "timeout": 30
    }
  }
}
```

Côté plugin (`src/lib.rs`, `Builder`, config parsée au runtime) :

```rust title="src/lib.rs"
use serde::Deserialize;
use tauri::{plugin::{Builder, TauriPlugin}, Runtime};

#[derive(Deserialize)]
pub struct Config {
  timeout: usize,
}

pub fn init<R: Runtime>() -> TauriPlugin<R, Config> {
  Builder::<R, Config>::new("<plugin-name>")
    .setup(|app, api| {
      let timeout = api.config().timeout;
      Ok(())
    })
    .build()
}
```

Voir `examples/tauri-conf-plugin.json` + `examples/lib-plugin.rs`.

## Lifecycle (index.mdx)

Hooks : `setup`, `on_navigation`, `on_webview_ready`, `on_event`, `on_drop` (+ mobiles dans `references/mobile.md`).

> - setup: Plugin is being initialized — Register mobile plugins, manage state, run background tasks
> - on_navigation: Web view is attempting to perform navigation — Validate the URL or track changes. Returning `false` cancels the navigation.
> - on_webview_ready: New window has been created — Execute an init script for every window
> - on_event: Event loop events — Handle core events such as window events and application exit requested (`docs.rs` `RunEvent`, jamais copié)
> - on_drop: Plugin is being deconstructed (`Drop`)

Voir `examples/lib-plugin.rs` (`setup` + `build`). API Rust linkée (`docs.rs`), jamais copiée.

## Exposer Rust + Commands (index.mdx)

> The plugin APIs defined in the project's `desktop.rs` and `mobile.rs` are exported to the user as a struct with the same name as the plugin (in pascal case). [...] through the extension trait defined in the plugin.

Exemple doc (`global-shortcut`) :

```rust title="src-tauri/src/lib.rs"
use tauri_plugin_global_shortcut::GlobalShortcutExt;

tauri::Builder::default()
  .plugin(tauri_plugin_global_shortcut::init())
  .setup(|app| {
    app.global_shortcut().register(...);
    Ok(())
  })
```

Commande (`src/commands.rs`, `AppHandle`/`Window` par injection, `Channel`, args comme une commande app — voir skill `tauri-ipc-bridge`) :

```rust title="src/commands.rs"
use tauri::{command, ipc::Channel, AppHandle, Runtime, Window};

#[command]
async fn upload<R: Runtime>(app: AppHandle<R>, window: Window<R>, on_progress: Channel, url: String) {
  // implement command logic here
  on_progress.send(100).unwrap();
}
```

Enregistrement (`src/lib.rs`) :

```rust title="src/lib.rs"
Builder::new("<plugin-name>")
    .invoke_handler(tauri::generate_handler![commands::upload])
```

Binding JS (`webview-src/index.ts`, `invoke('plugin:<plugin-name>|upload')`, build TS avant test) :

```js name="webview-src/index.ts"
import { invoke, Channel } from '@tauri-apps/api/core'

export async function upload(url: string, onProgressHandler: (progress: number) => void): Promise<void> {
  const onProgress = new Channel<number>()
  onProgress.onmessage = onProgressHandler
  await invoke('plugin:<plugin-name>|upload', { url, onProgress })
}
```

Voir `examples/commands-upload.rs` + `examples/guest-js-upload.js` + `examples/lib-plugin.rs`.
Check : `python3 scripts/check-plugin-dev.py --invoke examples/guest-js-upload.js`.

## State (index.mdx)

> A plugin can manage state in the same way a Tauri application does. Read the [State Management guide](/develop/state-management/) for more information.

Détail côté code : voir skill frère `tauri-ipc-bridge` (`State`, `manage`). Ici on ne duplique pas.
