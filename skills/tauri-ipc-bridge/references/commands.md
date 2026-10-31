# Commands — extrait doc

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/calling-rust.mdx` (titre `Calling Rust from the Frontend`)

## Definir (calling-rust.mdx)

> Tauri provides a simple yet powerful `command` system for calling Rust functions from your web app. Commands can accept arguments and return values. They can also return errors and be `async`.

> Command names must be unique.

> Commands defined in the `lib.rs` file cannot be marked as `pub` due to a limitation in the glue code generation.

Exemple canonique (meme fichier) : voir `examples/command-rust.rs`.

```rust title="src-tauri/src/lib.rs"
#[tauri::command]
fn my_custom_command() {
  println!("I was invoked from JavaScript!");
}
```

> You will have to provide a list of your commands to the builder function like so : `invoke_handler(tauri::generate_handler![my_custom_command])`.

Module separe (meme fichier) : `src-tauri/src/commands.rs` avec `pub fn`, enregistre `commands::my_custom_command`, l'invoke reste `invoke("my_custom_command")` (le prefixe `commands::` est ignore). Les noms restent uniques meme entre modules.

## Invoquer (meme fichier)

Voir `examples/command-frontend.js` :

```javascript
import { invoke } from '@tauri-apps/api/core';
invoke('my_custom_command');
```

> Arguments should be passed as a JSON object with camelCase keys : `invoke('my_custom_command', { invokeMessage: 'Hello!' })`. Avec `#[tauri::command(rename_all = "snake_case")]`, utiliser `invoke_message`.

> Arguments can be of any type, as long as they implement `serde::Deserialize`. Returned data can be of any type, as long as it implements `serde::Serialize`.

> Return values that implement `serde::Serialize` are serialized to JSON. To return array buffers in an optimized way, use `tauri::ipc::Response`.

## Erreurs (meme fichier)

> If your handler could fail, have the function return a `Result` : `Ok` resolve, `Err` reject. Everything returned from commands must implement `serde::Serialize`, including errors. En simple : `map_err(|err| err.to_string())`. En idiomatique : enum d'erreur avec `thiserror` + `impl serde::Serialize` manuelle.

## Async (meme fichier)

> Async commands are executed on a separate async task using `async_runtime::spawn`. Commands without the _async_ keyword are executed on the main thread unless defined with _#[tauri::command(async)]_.

> You cannot simply include borrowed arguments (`&str`, `State<'_, Data>`) in an async function (suivi : tauri-apps/tauri#2533). Option 1 : owned (`String`). Option 2 : retour `Result<a, b>` (ex `Result<String, ()>` avec `Ok(...)`).

## Contexte injectable (meme fichier)

- `WebviewWindow` : la webview appelante (`window.label()`).
- `AppHandle` : `path()`, shell, etc. Avec generique `R: Runtime` si runtime non-`wry` (voir `mock runtime`).
- `State` : voir `references/state.md`.
- `tauri::ipc::Request` : body brut + headers (`InvokeBody::Raw`, `headers().get("Authorization")`) ; cote JS : `invoke('upload', data, { headers })`.
- `tauri::ipc::Channel` : streaming, voir `references/events.md`.

## Multi-commandes (meme fichier)

> The `tauri::generate_handler!` macro takes an array of commands. To register multiple commands, you cannot call invoke_handler multiple times. Only the last call will be used.

API Rust linkee, jamais copiee : `Manager`, `App`, `State`, `Mutex`, `Arc`, `AppHandle`, `WebviewWindow`, `Listener`, `Emitter`, `Channel`, `Response`, `Request`, `async_runtime::spawn` (liens `docs.rs` en bas du fichier doc).
