# State — extrait doc

Source : `tauri-docs/src/content/docs/develop/state-management.mdx`, commit `ec113a50`, titre frontmatter `State Management`.

> In a Tauri application, you often need to keep track of the current state of your application or manage the lifecycle of things associated with it. Tauri provides an easy way to manage the state of your application using the `Manager` API, and read it when commands are called.

Exemple canonique (meme fichier) : voir `examples/state.rs`.

```rust
use tauri::{Builder, Manager};
struct AppData { welcome_message: &'static str }
Builder::default()
  .setup(|app| { app.manage(AppData { welcome_message: "Welcome to Tauri!" }); Ok(()) })
```

> You can later access your state with any type that implements the `Manager` trait, for example the `App` instance : `app.state::<AppData>()`.

## Mutabilite (meme fichier)

> In Rust, you cannot directly mutate values which are shared between multiple threads ... use interior mutability : `Mutex`. Lock, modify, drop (`MutexGuard` unlock auto).

> Contrary to popular belief, it is ok and often preferred to use the ordinary Mutex from the standard library in asynchronous code ... The primary use case for the async mutex is to provide shared mutable access to IO resources such as a database connection.

> You don't need to use `Arc` for things stored in `State` because Tauri will do this for you. Si `State` bloque un move vers un thread, mover un `AppHandle` (cheap clone) puis `state()` dedans.

## Acces (meme fichier)

Commandes : `fn increase_counter(state: State<'_, Mutex<AppState>>) -> u32`. Async Tokio : meme forme + `lock().await`, avec retour `Result<_, ()>` si arg emprunte (voir calling-rust Async). Hors commandes (thread, `on_window_event`) : `window.app_handle().state::<Mutex<AppState>>()` via le trait `Manager`.

## Types (meme fichier)

> If you use the wrong type for the `State` parameter, you will not get a compile time error. Instead, invoking the command fails at runtime: the `invoke` call is rejected with a `state not managed for field ...` error. Retrieving an unmanaged type directly with `Manager::state()` panics. Ex `State<'_, AppState>` au lieu de `State<'_, Mutex<AppState>>`.

Garde-fou doc : alias `type AppState = Mutex<AppStateInner>` (ne pas re-wrapp `Mutex` deux fois).

API Rust linkee, jamais copiee : `Manager`, `State`, `Mutex`, `Arc`, `App` (liens `docs.rs` en bas du fichier doc). Commandes : voir `references/commands.md`.
