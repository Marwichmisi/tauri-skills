# Support mobile `my-plugin` — commande `openCamera`

Source canonique : `tauri-docs/src/content/docs/develop/Plugins/develop-mobile.mdx` (titre `Mobile Plugin Development`), commit `ec113a50`, EN canonique seule.
Skill appliqué : `skills/tauri-plugin-dev` — routage `Ajouter mobile` → `references/mobile.md` → `examples/mobile-command.kt`, `examples/mobile-command.swift`, `examples/mobile-invoke.rs`, `examples/plugin-listener.js` → `scripts/check-plugin-dev.py --invoke`.

## 1. Android (Kotlin `@Command`)

Fichier : `outputs/mobile-command.kt` (dérivé de `examples/mobile-command.kt`).

```kotlin
@TauriPlugin
class MyPlugin(private val activity: Activity) : Plugin(activity) {
  @Command
  fun openCamera(invoke: Invoke) {
    val args = invoke.parseArgs(OpenCameraArgs::class.java)
    val ret = JSObject()
    ret.put("path", "/photo.jpg")
    invoke.resolve(ret)
    trigger("camera", payload)
  }
}
```

Doc : `A Tauri plugin for Android is defined as a Kotlin class that extends app.tauri.plugin.Plugin and is annotated with app.tauri.annotation.TauriPlugin. Each method annotated with app.tauri.annotation.Command can be called by Rust or JavaScript.`
Main-thread : `On Android native commands are scheduled on the main thread.` Pour IO bloquant : `CoroutineScope(Dispatchers.IO).launch { ... }`.
Init projet existant : `plugin android init` et `plugin ios init` (forme `develop-mobile.mdx` ; le guide desktop dit `plugin android add` / `plugin ios add` — citer la forme du fichier lu, ne jamais fusionner).

Args `InvokeArg` (requis / optionnel / défaut) — `outputs/mobile-command.kt` :

```kotlin
@InvokeArg
internal class OpenCameraArgs {
  lateinit var source: String      // requis : lateinit var Type
  var quality: Int? = null        // optionnel : var Type? = null
  var allowEdit: Boolean = false  // défaut : var Type = default-value
}
```

Doc : `Optional arguments are defined as var <argumentName>: Type? = null. Arguments with default values as var <argumentName>: Type = <default-value>. Required arguments as lateinit var <argumentName>: Type.`
Lecture : `invoke.parseArgs(OpenCameraArgs::class.java)`.

## 2. iOS (Swift `@objc`)

Fichier : `outputs/mobile-command.swift` (dérivé de `examples/mobile-command.swift`).

```swift
class MyPlugin: Plugin {
  @objc public func openCamera(_ invoke: Invoke) throws {
    invoke.resolve(["path": "/photo.jpg"])
    trigger("camera", data: ["path": "/photo.jpg"])
  }
}
```

Doc : `A Tauri plugin for iOS is defined as a Swift class that extends the Plugin class from the Tauri package. Each function with the @objc attribute and the (_ invoke: Invoke) parameter (for example @objc private func download(_ invoke: Invoke) { }) can be called by Rust or JavaScript.`
Package : `defined as a Swift package so that you can use its package manager to manage dependencies.`

Args `Decodable` — défaut NON supporté :

```swift
class OpenCameraArgs: Decodable {
  let source: String   // requis : let Type
  var quality: Int?    // optionnel : var Type?
  var allowEdit: Bool? // défaut : nullable + défaut posé dans la commande
}
// dans openCamera :
let allowEdit = args.allowEdit ?? false
```

Doc : `Optional arguments are defined as var <argumentName>: Type?. Arguments with default values are NOT supported. Use a nullable type and set the default value on the command function instead. Required arguments are defined as let <argumentName>: Type.`
Lecture : `try invoke.parseArgs(OpenCameraArgs.self)`.

## 3. Appel depuis Rust (`run_mobile_plugin`)

Fichier : `outputs/mobile-invoke.rs` (dérivé de `examples/mobile-invoke.rs`).

```rust
self.0.run_mobile_plugin("openCamera", payload).map_err(Into::into)
```

Forme complète (`CameraRequest` camelCase + `Photo`, `checkPermissions` / `requestPermissions`) :

```rust
pub fn open_camera(&self, payload: CameraRequest) -> crate::Result<Photo> {
  self.0.run_mobile_plugin("openCamera", payload).map_err(Into::into)
}
pub fn check_camera_permissions(&self) -> crate::Result<PermissionResponse> {
  self.0.run_mobile_plugin::<PermissionResponse>("checkPermissions", serde_json::Value::Null).map_err(Into::into)
}
pub fn request_camera_permissions(&self) -> crate::Result<PermissionResponse> {
  self.0.run_mobile_plugin::<PermissionResponse>("requestPermissions", serde_json::Value::Null).map_err(Into::into)
}
pub fn init<R: Runtime>() -> Builder<R> { Builder::new("my-plugin") }
```

Doc : template scindé `The default plugin template splits the plugin's implementation into two separate modules: desktop.rs and mobile.rs.` + `The mobile implementation sends a message to the native mobile code to execute a function and get a result back.` Logique partagée en `lib.rs` (`do_something`).
`PluginHandle::run_mobile_plugin` (docs.rs linké, jamais copié).
Appel Rust/JS : `run_mobile_plugin("openCamera", payload)` côté Rust ; `invoke('plugin:my-plugin|openCamera')` côté guest-js selon `references/plugin-basics.md`.

Calling Rust From Mobile (JNI/FFI, WebView suspendue) : `It is often preferable to write plugin code in Rust, for performance and reusability. While Tauri doesn't directly provide a mechanism to call Rust from your plugin code, using JNI on Android and FFI on iOS allows plugins to call shared code, even when the application WebView is suspended.` Android : crate `jni = "0.21"` sous `target.'cfg(target_os = "android")'.dependencies`, `System.loadLibrary("app_lib")`, `external fun` + `Java_com_example_HelloWorld_helloWorld` (`JNIEnv`, `JClass`, `JString`). iOS : `@_silgen_name` + `extern "C"` (`hello_world_ffi`, `free_hello_result_ffi`, `CStr`/`CString`). Blocs complets : voir fichier source `develop-mobile.mdx`, linkés ici.

## 4. Permissions mobiles (auto)

`Tauri automatically implements two commands for the plugin: checkPermissions and requestPermissions. Those commands can be directly called from JavaScript or Rust.`

- Android : annotation `@TauriPlugin(permissions = [Permission(...)])`, alias ; override iOS `checkPermissions` / `requestPermissions` uniquement si permissions custom (voir fichier source pour snippets complets).
- Sans override, appeler directement `run_mobile_plugin::<PermissionResponse>("requestPermissions" | "checkPermissions")` (Rust, `PermissionState`, `rename_all camelCase`) ou `invoke('plugin:my-plugin|checkPermissions')` (JS, `PermissionState`, `prompt-with-rationale`, `startsWith('prompt')`).
- Cet ajout ne crée aucun `permissions/*.toml` côté auteur ; la `capability` côté app reste du ressort de `tauri-security-capabilities` (voir Frontières).

## 5. Events (`trigger` + `addPluginListener`)

Natif — `Plugins can emit events at any point of time using the trigger function.` :

```kotlin
trigger("camera", payload)              // Android : trigger("load", JSObject())
trigger("camera", data: ["path": ...])  // iOS : trigger("load", data: [:])
```

Écoute JS — fichier `outputs/plugin-listener.js` (dérivé de `examples/plugin-listener.js`) — alias compact `addPluginListener('my-plugin','camera')` :

```javascript
import { addPluginListener, PluginListener } from '@tauri-apps/api/core';
export async function onCamera(handler) {
  return await addPluginListener('my-plugin', 'camera', handler);
}
```

Doc :

```javascript
import { addPluginListener, PluginListener } from '@tauri-apps/api/core';
export async function onRequest(handler): Promise<PluginListener> {
  return await addPluginListener('<plugin-name>', 'event-name', handler);
}
```

Capability obligatoire : `Listening to plugin events from JavaScript is gated by the same capability and permission system that gates plugin commands. Add the plugin's permission (commonly <plugin-name>:default, or a specific allow-listen-* permission if the plugin defines one) to the permissions array of a capability under src-tauri/capabilities/.`
Concrètement : ajouter `my-plugin:default` (forme `<plugin>:default`, donc `<plugin-name>:default`) dans `permissions: [...]` d'une capability `src-tauri/capabilities/*.json`. Toute la doctrine capability côté app vit chez `tauri-security-capabilities` — ce skill ne la duplique pas, il la pointe.

## 6. Pages 16KB Android

`Google is moving to make 16KB memory pages a requirement in all new Android app submissions. Building with an NDK version 28 or higher should automatically generate bundles that meet this requirement, but in the event an older NDK version must be used or generated files aren't 16KB aligned, the following can be added to .cargo/config.toml to flag this to rustc.`

Fichier : `outputs/cargo-config.toml` (à placer en `.cargo/config.toml`, seulement si NDK < 28) :

```toml
[target.aarch64-linux-android]
rustflags = ["-C", "link-arg=-Wl,-z,max-page-size=16384"]
```

NDK >= 28 : rien à faire.

## 7. Validation `scripts/check-plugin-dev.py --invoke`

```
$ python3 scripts/check-plugin-dev.py --invoke outputs/mobile-invoke.rs
OK outputs/mobile-invoke.rs: invoke plugin fidèle
 - Builder::new("my-plugin")
 - run_mobile_plugin("checkPermissions")
 - run_mobile_plugin("openCamera")
 - run_mobile_plugin("requestPermissions")

$ python3 scripts/check-plugin-dev.py --invoke outputs/plugin-listener.js
OK outputs/plugin-listener.js: invoke plugin fidèle
 - addPluginListener('my-plugin', 'camera')

$ python3 scripts/check-plugin-dev.py --identifier my-plugin
OK identifier 'my-plugin' valide (develop/Plugins/index.mdx)
```

Kotlin/Swift : fidélité doc visuelle (`@Command openCamera`, `@objc openCamera`, `InvokeArg`/`Decodable`, `trigger("camera", ...)`), le checker `--invoke` couvre `run_mobile_plugin` / `addPluginListener` côté Rust/JS (cf. `SKILL.md` : `Valider avec python3 scripts/check-plugin-dev.py --invoke examples/mobile-invoke.rs et --invoke examples/plugin-listener.js`).

## 8. Frontières inter-skills

- `tauri-security-capabilities` : seule autorité capabilities/permissions côté app (`capabilities/*.json`, `my-plugin:default` dans `permissions: [...]`, `deny` > `allow`, CSP/asset-protocol). Ici côté auteur mobile (`trigger`/`addPluginListener`) ; l'écoute JS exige `my-plugin:default` en capability — doctrine là-bas.
- `tauri-ipc-bridge` : implémentation commands/events/state/resources/sidecar côté app (`#[tauri::command]`, `invoke_handler` app, `Channel`, `State`). Ici côté plugin (`mobile.rs`/`desktop.rs` via `Builder`, `run_mobile_plugin("openCamera")`).
- `tauri-plugins-catalogue` : fiches usage des 30 plugins. Ici auteur (création).
- `tauri-config-cli-reference` : schéma `tauri.conf.json`, CLI (`plugin new/android/ios`, ici `plugin android init` / `plugin ios init` forme mobile), env-vars. Ici seulement `plugins.my-plugin` + `platforms.support`.
- `tauri-start`, `tauri-migrate`, `tauri-core-concepts`, `tauri-dev-quality`, `tauri-distribution`, `tauri-ui-recettes`, `tauri-frontend-bindings` : hors périmètre ; renvoyer si le besoin y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).
