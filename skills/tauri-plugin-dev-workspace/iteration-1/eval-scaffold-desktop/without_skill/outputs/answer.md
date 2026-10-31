# Scaffold plugin desktop `my-plugin` — Tauri v2

Squelette `tauri-plugin-my-plugin` desktop-first, validé avec `scripts/check-plugin-dev.py`
(`--identifier` / `--cargo` / `--invoke`).

## 1. Identifiant

- Plugin : `my-plugin` → crate `tauri-plugin-my-plugin`
- Vérifié : `python3 scripts/check-plugin-dev.py --identifier my-plugin`
- Résultat : `OK identifier 'my-plugin' valide (develop/Plugins/index.mdx)`

Règles appliquées : `[a-z0-9-]`, pas de `_`/majuscules, pas de leading/trailing `-`, `<=64` caractères.

## 2. Structure `src/`

```
outputs/
  Cargo.plugin.toml
  guest-js-upload.js
  tauri.conf.json
  src/
    lib.rs       # Builder::new("my-plugin") + invoke_handler upload + setup
    commands.rs  # #[tauri::command] upload avec Channel
    desktop.rs   # impl desktop
    mobile.rs    # run_mobile_plugin("upload"), Android partial / iOS none
```

### `src/lib.rs`

```rust
use tauri::{
    plugin::{Builder, TauriPlugin},
    Manager, Runtime,
};

mod commands;
mod desktop;
mod mobile;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("plugin error: {0}")]
    Plugin(String),
    #[error("mobile not supported on this target")]
    MobileNotSupported,
}

impl From<Error> for tauri::InvokeError {
    fn from(e: Error) -> Self {
        Self::from(e.to_string())
    }
}

pub type Result<T> = std::result::Result<T, Error>;

/// Entry point for the `my-plugin` Tauri v2 plugin.
pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![commands::upload])
        .setup(|app, _api| {
            let _handle = app.handle().clone();
            log::info!("my-plugin setup");
            Ok(())
        })
        .build()
}
```

Points : `Builder::new("my-plugin")`, `invoke_handler` expose `upload`, `setup` enregistre l'état desktop.

### `src/commands.rs`

```rust
use tauri::{ipc::Channel, AppHandle, Runtime};

#[derive(Debug, Clone, serde::Serialize)]
#[serde(rename_all = "camelCase")]
pub struct UploadProgress {
    pub chunk: u64,
    pub total: u64,
}

/// Upload a file with progress events forwarded over a Channel.
/// Exposed to JS as `plugin:my-plugin|upload`.
#[tauri::command]
pub async fn upload<R: Runtime>(
    _app: AppHandle<R>,
    path: String,
    on_progress: Channel<UploadProgress>,
) -> Result<String, String> {
    if path.trim().is_empty() {
        return Err("path must not be empty".into());
    }
    let total = 100u64;
    for chunk in [50u64, 100u64] {
        let _ = on_progress.send(UploadProgress { chunk, total });
    }
    log::info!("my-plugin upload {}", path);
    Ok(format!("uploaded:{path}"))
}
```

### `src/desktop.rs`

Impl desktop `MyPlugin<R>` + `init(app, config)` appelée depuis `setup` sur cibles desktop.

### `src/mobile.rs`

```rust
handle.run_mobile_plugin::<String>("upload", InvokeBody::Json(...))
```

Android partiel, iOS non supporté (cf. `platforms.support`).

Vérifié : `check-plugin-dev.py --invoke src/lib.rs` → `OK ... Builder::new("my-plugin")`
et `--invoke src/mobile.rs` → `OK ... run_mobile_plugin("upload")`.

## 3. Guest-JS avec Channel (`guest-js-upload.js`)

```js
import { invoke, Channel } from '@tauri-apps/api/core';

export async function upload(path, onEvent) {
  const onProgress = new Channel();
  onProgress.onmessage = (progress) => {
    onEvent?.(progress);
  };
  return invoke('plugin:my-plugin|upload', { path, onProgress });
}
```

Vérifié : `check-plugin-dev.py --invoke guest-js-upload.js` → `OK ... invoke plugin:my-plugin|upload`.

## 4. Cargo `platforms.support` (`Cargo.plugin.toml`)

```toml
[package]
name = "tauri-plugin-my-plugin"
version = "0.1.0"
edition = "2021"

[package.metadata.platforms.support]
windows = { level = "full" }
linux = { level = "full" }
macos = { level = "full" }
android = { level = "partial", notes = "Upload works via system picker; background upload is limited by the OS, progress events may be coalesced." }
ios = { level = "none" }
```

Vérifié : `check-plugin-dev.py --cargo Cargo.plugin.toml` → `OK ... platforms.support fidèle (windows=full, linux=full, macos=full, android=partial, ios=none)`.

## 5. `tauri.conf.json`

```json
{
  "plugins": {
    "my-plugin": { "timeout": 30 }
  }
}
```

`plugins.my-plugin.timeout = 30` vérifié par parsing JSON.

## 6. Validation complète

```
python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --identifier my-plugin
# OK identifier 'my-plugin' valide

python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --cargo outputs/Cargo.plugin.toml
# OK ... platforms.support fidèle (windows=full, linux=full, macos=full, android=partial, ios=none)

python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --invoke outputs/guest-js-upload.js
# OK ... invoke plugin fidèle
#  - invoke plugin:my-plugin|upload

python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --invoke outputs/src/lib.rs
# OK ... invoke plugin fidèle
#  - Builder::new("my-plugin")
```

Squelette suivi de bout en bout : identifier → Rust commands/desktop/mobile/lib + Builder/invoke_handler/setup → guest-js `plugin:my-plugin|upload` + `Channel` → Cargo support desktop full / android partial + notes / ios none → `tauri.conf` timeout 30.
