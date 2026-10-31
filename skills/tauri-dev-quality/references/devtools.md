# DevTools CrabNebula — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Debug/crabnebula-devtools.mdx` (titre `CrabNebula DevTools`)

> [CrabNebula](https://crabnebula.dev/) provides a free [DevTools](https://crabnebula.dev/devtools/) application for Tauri as part of its partnership with the Tauri project. This application allows you to instrument your Tauri app by capturing its embedded assets, Tauri configuration file, logs and spans and providing a web frontend to seamlessly visualize data in real time.

> With the CrabNebula DevTools you can inspect your app's log events (including logs from dependencies), track down the performance of your command calls and overall Tauri API usage, with a special interface for Tauri events and commands, including payload, responses and inner logs and execution spans.

## Setup (même fichier)

```sh
cargo add tauri-plugin-devtools@2.0.0
```

Voir `examples/crabnebula-devtools.rs` (copie exacte) : `tauri_plugin_devtools::init()` le plus tôt possible dans `main`, `builder.plugin(devtools)` sous `#[cfg(debug_assertions)]` uniquement (recommandé doc). Lancer l'app : message DevTools en console si OK.

```rust
fn main() {
    // This should be called as early in the execution of the app as possible
    #[cfg(debug_assertions)] // only enable instrumentation in development builds
    let devtools = tauri_plugin_devtools::init();
    let mut builder = tauri::Builder::default();
    #[cfg(debug_assertions)]
    {
        builder = builder.plugin(devtools);
    }
    builder
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

Détails : voir docs CrabNebula (`docs.crabnebula.dev/devtools/get-started/`), hors source-de-vérité locale.
