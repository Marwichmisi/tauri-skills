# Plugin mobile — Android (Kotlin), iOS (Swift), FFI, permissions, events

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Plugins/develop-mobile.mdx` (titre `Mobile Plugin Development`)

> Be sure that you're familiar with the concepts covered in the [Plugin Development guide](/develop/plugins/) as many concepts in this guide build on top of foundations covered there.

> Plugins can run native mobile code written in Kotlin (or Java) and Swift. The default plugin template includes an Android library project using Kotlin and a Swift package including an example mobile command showing how to trigger its execution from Rust code.

## Init mobile (develop-mobile.mdx)

> Follow the steps in the [Plugin Development guide](/develop/plugins/#initialize-plugin-project) to initialize a new plugin project.

> If you have an existing plugin and would like to add Android or iOS capabilities to it, you can use `plugin android init` and `plugin ios init` to bootstrap the mobile library projects and guide you through the changes needed.

Note fidélité : le guide desktop dit `plugin android add` / `plugin ios add` pour le même besoin (`references/plugin-basics.md`). Citer la forme du fichier lu, ne pas fusionner ni inventer.

> The default plugin template splits the plugin's implementation into two separate modules: `desktop.rs` and `mobile.rs`.

> The desktop implementation uses Rust code to implement a functionality, while the mobile implementation sends a message to the native mobile code to execute a function and get a result back. If shared logic is needed across both implementations, it can be defined in `lib.rs`.

```rust title="src/lib.rs"
use tauri::Runtime;

impl<R: Runtime> <plugin-name><R> {
  pub fn do_something(&self) {
    // do something that is a shared implementation between desktop and mobile
  }
}
```

### Android (develop-mobile.mdx)

> A Tauri plugin for Android is defined as a Kotlin class that extends `app.tauri.plugin.Plugin` and is annotated with `app.tauri.annotation.TauriPlugin`. Each method annotated with `app.tauri.annotation.Command` can be called by Rust or JavaScript.

> Tauri uses Kotlin by default for the Android plugin implementation, but you can switch to Java if you prefer. After generating a plugin, right click the Kotlin plugin class in Android Studio and select the "Convert Kotlin file to Java file" option from the menu.

Voir `examples/mobile-command.kt`.

### iOS (develop-mobile.mdx)

> A Tauri plugin for iOS is defined as a Swift class that extends the `Plugin` class from the `Tauri` package. Each function with the `@objc` attribute and the `(_ invoke: Invoke)` parameter (for example `@objc private func download(_ invoke: Invoke) { }`) can be called by Rust or JavaScript.

> The plugin is defined as a [Swift package](https://www.swift.org/package-manager/) so that you can use its package manager to manage dependencies.

Voir `examples/mobile-command.swift`.

## Plugin Configuration mobile (develop-mobile.mdx)

> Refer to the [Plugin Configuration section](/develop/plugins/#plugin-configuration) of the Plugin Development guide for more details on developing plugin configurations.

Getter config côté mobile (`getConfig` / `parseConfig`, `timeout` doc) : voir fichier source pour les snippets Kotlin/Swift complets. Ici on ne duplique pas, on renvoie au fichier.

## Lifecycle mobile (develop-mobile.mdx)

Hooks : `load`, `onNewIntent` (Android seul) + lifecycles plugin du guide desktop.

> - load: When the plugin is loaded into the web view — Execute plugin initialization code
> - onNewIntent: Android only, when the activity is re-launched ([Activity#onNewIntent](https://developer.android.com/...)) — Handle re-launch (notification, deep link).

Snippets `load(webView)` / `load(webview:)` et `onNewIntent(intent)` : voir fichier source. API Android/iOS linkées, jamais copiées hors extraits.

## Adding Mobile Commands (develop-mobile.mdx)

Classe plugin par plateforme (commandes appelables depuis Rust) : voir `examples/mobile-command.kt` + `examples/mobile-command.swift`.

Android (`@Command`, `Invoke`, `JSObject`, main-thread + coroutines) :

```kotlin
@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  @Command
  fun openCamera(invoke: Invoke) {
    val ret = JSObject()
    ret.put("path", "/photo.jpg")
    invoke.resolve(ret)
  }
}
```

> On Android native commands are scheduled on the main thread. Performing long-running operations will cause the UI to freeze and potentially "Application Not Responding" (ANR) error. If you need to wait for some blocking IO, you can launch a coroutine like `CoroutineScope(Dispatchers.IO).launch { ... }`.

`suspend` exige un scope custom (`CoroutineScope(Dispatchers.Default + SupervisorJob())`, `Dispatchers.IO` pour fetch) : voir fichier source.

iOS (`@objc`, `invoke.resolve`) : voir `examples/mobile-command.swift`.

Appel depuis Rust (`PluginHandle::run_mobile_plugin`, `docs.rs` linké) :

```rust
self.0.run_mobile_plugin("openCamera", payload).map_err(Into::into)
```

Voir `examples/mobile-invoke.rs`.
Check : `python3 scripts/check-plugin-dev.py --invoke examples/mobile-invoke.rs`.

## Command Arguments (develop-mobile.mdx)

Android : classe `@app.tauri.annotation.InvokeArg`, inner objects annotés aussi.

```kotlin
@InvokeArg
internal class OpenAppArgs {
  lateinit var name: String
  var timeout: Int? = null
}
```

> Optional arguments are defined as `var <argumentName>: Type? = null`. Arguments with default values as `var <argumentName>: Type = <default-value>`. Required arguments as `lateinit var <argumentName>: Type`.

iOS : classe `Decodable`, inner `Decodable`.

```swift
class OpenArgs: Decodable {
  let requiredArg: String
  var allowEdit: Bool?
  var app: OpenAppArgs?
}
```

> Optional arguments are defined as `var <argumentName>: Type?`. Arguments with default values are **NOT** supported. Use a nullable type and set the default value on the command function instead. Required arguments are defined as `let <argumentName>: Type`.

Lecture : `invoke.parseArgs(OpenArgs::class.java)` (Android) / `try invoke.parseArgs(OpenArgs.self)` (iOS). Voir fichier source pour les blocs complets.

## Calling Rust From Mobile (develop-mobile.mdx)

> It is often preferable to write plugin code in Rust, for performance and reusability. While Tauri doesn't directly provide a mechanism to call Rust from your plugin code, using JNI on Android and FFI on iOS allows plugins to call shared code, even when the application WebView is suspended.

Android : crate `jni = "0.21"` sous `target.'cfg(target_os = "android")'.dependencies`, `System.loadLibrary("app_lib")`, `external fun helloWorld(name: String): String?` + `Java_com_example_HelloWorld_helloWorld` côté Rust (`JNIEnv`, `JClass`, `JString`). iOS : `@_silgen_name` + `extern "C"` (`hello_world_ffi`, `free_hello_result_ffi`, `CStr`/`CString`). Voir fichier source pour les blocs JNI/FFI complets — linkés ici, jamais réinventés.

## Android 16KB Memory Pages (develop-mobile.mdx)

> Google is moving to make 16KB memory pages a requirement in all new Android app submissions. Building with an NDK version 28 or higher should automatically generate bundles that meet this requirement, but in the event an older NDK version must be used or generated files aren't 16KB aligned, the following can be added to `.cargo/config.toml` to flag this to `rustc`.

```toml
[target.aarch64-linux-android]
rustflags = ["-C", "link-arg=-Wl,-z,max-page-size=16384"]
```

## Permissions mobile (develop-mobile.mdx)

Annotation Android (`@TauriPlugin(permissions = [Permission(...)])`, alias) / override iOS (`checkPermissions` / `requestPermissions`) : voir fichier source.

> Tauri automatically implements two commands for the plugin: `checkPermissions` and `requestPermissions`. Those commands can be directly called from JavaScript or Rust.

JS (`invoke('plugin:<plugin-name>|checkPermissions')`, `PermissionState`, `prompt-with-rationale`, `startsWith('prompt')`) et Rust (`run_mobile_plugin::<PermissionResponse>("requestPermissions" | "checkPermissions")`, `PermissionState`, `rename_all camelCase`) : voir fichier source pour les blocs complets.

## Plugin Events (develop-mobile.mdx)

> Plugins can emit events at any point of time using the `trigger` function.

Android (`trigger("load", JSObject())`, `trigger("camera", payload)`) / iOS (`trigger("load", data: [:])`) : voir fichier source.

Écoute NPM (`addPluginListener`, `docs.rs`/`reference/javascript` linkés) :

```javascript
import { addPluginListener, PluginListener } from '@tauri-apps/api/core';

export async function onRequest(
  handler: (url: string) => void
): Promise<PluginListener> {
  return await addPluginListener('<plugin-name>', 'event-name', handler);
}
```

Voir `examples/plugin-listener.js`.
Check : `python3 scripts/check-plugin-dev.py --invoke examples/plugin-listener.js`.

> Listening to plugin events from JavaScript is gated by the same [capability](/security/capabilities/) and [permission](/security/permissions/) system that gates plugin commands. Add the plugin's permission (commonly `<plugin-name>:default`, or a specific `allow-listen-*` permission if the plugin defines one) to the `permissions` array of a capability under `src-tauri/capabilities/`.

Frontière : toute capability/permission côté app remonte à `tauri-security-capabilities` (`<plugin-name>:default` dans `permissions: [...]`, voir `examples/` de ce skill pour la forme). Ici côté auteur mobile (trigger/listen).
