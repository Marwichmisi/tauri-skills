# Support mobile `my-plugin` — commande `openCamera`

## 1. Android — Kotlin `@Command` (`android/src/main/java/com/plugin/myplugin/MyPlugin.kt`)

```kotlin
package com.plugin.myplugin

import android.app.Activity
import app.tauri.plugin.Command
import app.tauri.plugin.Invoke
import app.tauri.plugin.Plugin
import app.tauri.plugin.JSObject

class MyPluginPlugin(activity: Activity) : Plugin(activity) {

    @Command
    fun openCamera(invoke: Invoke) {
        // requis : quality
        val quality = invoke.getString("quality")
            ?: return invoke.reject("quality est requis")
        // optionnel : flash (nullable)
        val flash = invoke.getBoolean("flash") // null si absent
        // défaut : mode = "auto" si absent
        val mode = invoke.getString("mode", "auto")!!

        // ... ouvrir la caméra avec quality/flash/mode ...

        val ret = JSObject()
        ret.put("path", "/tmp/photo.jpg")
        ret.put("quality", quality)
        invoke.resolve(ret)
    }

    // checkPermissions / requestPermissions sont fournis
    // automatiquement par la classe Plugin dès que les
    // permissions sont déclarées (voir §4).
    // Pas besoin de les réécrire sauf logique custom.
}
```

Déclaration Android dans `android/src/main/AndroidManifest.xml` :

```xml
<uses-permission android:name="android.permission.CAMERA" />
```

Enregistrement dans `src/mobile.rs` côté Rust (plugin id `my-plugin`).

## 2. iOS — Swift `@objc` + `Decodable` (`ios/Sources/MyPluginPlugin.swift`)

```swift
import Tauri

struct OpenCameraArgs: Decodable {
    let quality: String       // requis : decode échoue si absent
    let flash: Bool?          // optionnel : nil si absent
    var mode: String = "auto" // défaut via extension ou decodeIfPresent
}

extension OpenCameraArgs {
    enum CodingKeys: String, CodingKey {
        case quality, flash, mode
    }
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        quality = try c.decode(String.self, forKey: .quality)
        flash = try c.decodeIfPresent(Bool.self, forKey: .flash)
        mode = try c.decodeIfPresent(String.self, forKey: .mode) ?? "auto"
    }
}

class MyPluginPlugin: Plugin {
    @objc func openCamera(_ invoke: Invoke) throws {
        let args = try invoke.parseArgs(OpenCameraArgs.self)
        // ... ouvrir la caméra ...
        invoke.resolve(["path": "/tmp/photo.jpg", "quality": args.quality])
    }
    // checkPermissions / requestPermissions : auto via Plugin de base.
}
```

Permission iOS dans `ios/MyPlugin-Info.plist` :

```xml
<key>NSCameraUsageDescription</key>
<string>my-plugin a besoin de la caméra</string>
```

## 3. Rust — `run_mobile_plugin` + args (`src/mobile.rs` + `src/commands.rs`)

```rust
use serde::{Deserialize, Serialize};
use tauri::{AppHandle, Runtime};

fn default_mode() -> String { "auto".to_string() }

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct OpenCameraArgs {
    pub quality: String,              // requis
    pub flash: Option<bool>,          // optionnel
    #[serde(default = "default_mode")]
    pub mode: String,                 // défaut = "auto"
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CameraResult {
    pub path: String,
}

#[tauri::command]
pub async fn open_camera<R: Runtime>(
    app: AppHandle<R>,
    args: OpenCameraArgs,
) -> Result<CameraResult, String> {
    #[cfg(mobile)]
    {
        app.run_mobile_plugin("openCamera", args)
            .map_err(|e| e.to_string())
    }
    #[cfg(not(mobile))]
    {
        let _ = app;
        Err("openCamera n'est supporté que sur mobile".into())
    }
}
```

`src/lib.rs` (extrait) :

```rust
use tauri::{Runtime, plugin::TauriPlugin};

pub fn init<R: Runtime>() -> TauriPlugin<R> {
    tauri::plugin::Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![commands::open_camera])
        .setup(|app, _api| {
            #[cfg(mobile)]
            let _handle = app.register_mobile_plugin(
                "com.plugin.myplugin",
                "MyPluginPlugin",
            )?;
            Ok(())
        })
        .build()
}
```

> `invoke('plugin:my-plugin|openCamera', args)` côté guest-js est routé
> vers `open_camera` sur desktop et vers le plugin natif via
> `run_mobile_plugin("openCamera", …)` sur mobile.

## 4. Permissions `checkPermissions` / `requestPermissions` (auto)

Aucun code Kotlin/Swift à écrire : Tauri génère ces deux commandes
dès que le plugin déclare des permissions mobiles.

```toml
# permissions/mobile_camera.toml (exemple)
[[permission]]
identifier = "camera"
description = "Permet d'ouvrir la caméra"
```

```js
// guest-js : les commandes existent sans code natif supplémentaire
import { invoke } from '@tauri-apps/api/core';
await invoke('plugin:my-plugin|checkPermissions');
await invoke('plugin:my-plugin|requestPermissions', { permissions: ['camera'] });
await invoke('plugin:my-plugin|openCamera', { quality: 'hd' });
```

## 5. Event `camera` — `trigger` (Rust) + `addPluginListener` (JS)

Rust — émettre après capture (ex. dans `mobile.rs` ou après `open_camera`) :

```rust
use tauri::Emitter; // ou plugin trigger selon version

app.trigger("my-plugin://camera", serde_json::json!({
    "path": "/tmp/photo.jpg"
}))?;
```

JS — écoute :

```js
import { addPluginListener } from '@tauri-apps/api/core';

const unlisten = await addPluginListener('my-plugin', 'camera', (event) => {
  console.log('photo:', event.payload.path);
});
```

## 6. Page-size 16 Ko (seulement si NDK < 28)

NDK r28+ aligne déjà sur 16 Ko (Android 15+ l'exige). Si NDK ≤ r27,
forcer dans `.cargo/config.toml` :

```toml
# .cargo/config.toml
[target.aarch64-linux-android]
rustflags = ["-C", "link-args=-Wl,-z,max-page-size=16384"]

[target.armv7-linux-androideabi]
rustflags = ["-C", "link-args=-Wl,-z,max-page-size=16384"]

[target.i686-linux-android]
rustflags = ["-C", "link-args=-Wl,-z,max-page-size=16384"]

[target.x86_64-linux-android]
rustflags = ["-C", "link-args=-Wl,-z,max-page-size=16384"]
```

## 7. Validation

```bash
python3 scripts/check-plugin-dev.py --invoke path/to/mobile.rs
python3 scripts/check-plugin-dev.py --invoke path/to/MyPlugin.kt
python3 scripts/check-plugin-dev.py --invoke path/to/MyPluginPlugin.swift
python3 scripts/check-plugin-dev.py --invoke path/to/listener.js
```

Corriger jusqu'au vert avant de merger.

## 8. Rappel capability (délégué à `tauri-security-capabilities`)

L'écoute JS via `addPluginListener('my-plugin', 'camera', …)` ne reçoit
rien sans permission côté app. Ajouter le set par défaut dans la
capability :

```json
{
  "permissions": ["my-plugin:default"]
}
```

Le détail capabilities/permissions côté app (deny > allow, scopes,
CSP) est l'autorité de `tauri-security-capabilities`, pas d'ici.
