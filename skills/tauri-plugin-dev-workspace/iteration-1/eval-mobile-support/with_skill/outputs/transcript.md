# Transcript — eval mobile-support (with_skill)

## 1. Lecture skill
- Lu `skills/tauri-plugin-dev/SKILL.md` (workflow + routage + frontières + règle anti-drift).
- Intention détectée : `Ajouter mobile` → ligne routage `Ajouter mobile (Kotlin @Command, Swift @objc, run_mobile_plugin, args, JNI/FFI, 16KB, checkPermissions, trigger/addPluginListener)`.

## 2. Routage references
- Lu `skills/tauri-plugin-dev/references/mobile.md` (Source commit `ec113a50`, titre `Mobile Plugin Development`, fichier `develop/Plugins/develop-mobile.mdx`).
- Extraits retenus : classe Android `extends Plugin` + `@TauriPlugin`/`@Command`/`Invoke`/`JSObject` + main-thread/coroutines ; classe iOS `extends Plugin` + `@objc (_ invoke: Invoke)` + Swift package ; `desktop.rs`/`mobile.rs` + `lib.rs do_something` ; `run_mobile_plugin("openCamera", payload)` ; `InvokeArg` (lateinit requis / `? = null` optionnel / `= default` défaut) + `invoke.parseArgs(...::class.java)` ; `Decodable` (`let` requis / `var ?` optionnel / défaut NOT supported → nullable + défaut en commande) + `try invoke.parseArgs(... .self)` ; JNI `jni 0.21` + `System.loadLibrary` / FFI `@_silgen_name` + `extern C` ; 16KB `NDK >= 28 auto` sinon `.cargo/config.toml rustflags max-page-size=16384` ; `checkPermissions`/`requestPermissions` auto (`Tauri automatically implements...`) ; `trigger("camera", ...)` + `addPluginListener('<plugin-name>','event-name')` + gate `commonly <plugin-name>:default ... under src-tauri/capabilities/`.

## 3. Application exemples
- Lus `examples/mobile-command.kt`, `examples/mobile-command.swift`, `examples/mobile-invoke.rs`, `examples/plugin-listener.js`, `scripts/check-plugin-dev.py`.
- Vérifié `check-plugin-dev.py --invoke` OK sur exemples (`run_mobile_plugin("openCamera")`, `addPluginListener('my-plugin','camera')`).
- Produit artefacts enrichis :
  - `outputs/mobile-command.kt` : `@Command fun openCamera` + `OpenCameraArgs @InvokeArg` (source requis / quality optionnel / allowEdit défaut) + `parseArgs` + `resolve` + `trigger("camera", payload)`.
  - `outputs/mobile-command.swift` : `OpenCameraArgs: Decodable` (let/var ?/nullable+défaut commande) + `@objc public func openCamera(_ invoke: Invoke)` + `parseArgs` + `resolve` + `trigger("camera", data:)`.
  - `outputs/mobile-invoke.rs` : `CameraRequest` camelCase + `Photo` + `open_camera` via `run_mobile_plugin("openCamera")` + `check/request_camera_permissions` via `run_mobile_plugin("checkPermissions"/"requestPermissions")` + `Builder::new("my-plugin")`.
  - `outputs/plugin-listener.js` : `addPluginListener('my-plugin','camera', handler)`.
  - `outputs/cargo-config.toml` : contenu `.cargo/config.toml` 16KB (si NDK<28).
  - `outputs/answer.md` : réponse complète avec pointeurs source + frontière `tauri-security-capabilities` (`my-plugin:default` en capability).

## 4. Validation
- `python3 scripts/check-plugin-dev.py --invoke outputs/mobile-invoke.rs` → OK (Builder + 3× run_mobile_plugin).
- `python3 scripts/check-plugin-dev.py --invoke outputs/plugin-listener.js` → OK (addPluginListener my-plugin/camera).
- `python3 scripts/check-plugin-dev.py --identifier my-plugin` → OK.
- Kotlin/Swift : fidélité doc (checker --invoke couvre Rust/JS per SKILL.md).

## 5. Frontière rappelée
- Écoute JS exige `my-plugin:default` (`<plugin>:default`) en capability → doctrine `tauri-security-capabilities`. Cité `develop/Plugins/develop-mobile.mdx` commit `ec113a50`.
