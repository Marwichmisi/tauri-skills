# Splashscreen + Mobile — baseline (without skill)

## 1. Fenêtres (`tauri.conf.json`)

Deux fenêtres :
- `main` : `url: "/"`, `visible: false` (hidden au démarrage, affichée après init).
- `splashscreen` : `url: "splashscreen.html"`, `visible: true`, `decorations: false`, 400x200, centrée.

Voir `tauri.conf.json` (section `app.windows`).

## 2. Rust — SetupState + `set_complete` + close/show + `tokio::time`

Voir `splashscreen.rs` :

- `SetupState { complete: AtomicBool }` enregistré via `app.manage(...)`.
- Commande `set_complete` : `state.set_complete()`, puis `get_webview_window("splashscreen").close()` et `get_webview_window("main").show()`.
- Fallback avec `tokio::time::sleep(5s)` dans `spawn_splash_fallback` : si le frontend n'a pas appelé `set_complete`, on force `close` / `show`.
- Enregistrer dans le builder : `.manage(SetupState::new())` + `.invoke_handler![set_complete]` + `.setup(init_setup)`.

`lib.rs` minimal :

```rust
mod splashscreen;
mod mobile;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let mut app = tauri::Builder::default()
        .manage(splashscreen::SetupState::new())
        .invoke_handler(tauri::generate_handler![splashscreen::set_complete])
        .setup(|app| splashscreen::init_setup(app))
        .build(tauri::generate_context!())
        .expect("error while building tauri app");
    mobile::run_with_file_associations(app);
}
```

## 3. Capability — `allow-create-webview-window`

Frontend `mobile.js` crée une fenêtre dynamique (`new WebviewWindow(...)`), donc le frontend a besoin de la permission.

`capabilities/mobile.json` (ou `default.json`) :

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "mobile-cap",
  "windows": ["main", "second"],
  "permissions": [
    "core:default",
    "core:window:allow-create-webview-window",
    "core:window:allow-show",
    "core:window:allow-close"
  ]
}
```

Sans `allow-create-webview-window`, `new WebviewWindow` échoue avec `tauri://error`.

## 4. `WebviewWindow` + `activityName` (Android)

Voir `mobile.js` :

```js
import { WebviewWindow } from "@tauri-apps/api/webviewWindow";
const second = new WebviewWindow("second", {
  url: "/second",
  activityName: "com.example.splashmobile.SecondActivity",
});
```

`activityName` permet de cibler une Activity Android personnalisée pour cette fenêtre.

## 5. `fileAssociations` png/jpg + `RunEvent::Opened` cold/warm

`tauri.conf.json` → `bundle.fileAssociations` avec `ext: ["png"]` et `ext: ["jpg", "jpeg"]`, `mimeType: image/png` / `image/jpeg`, `role: Viewer`.

Rust (`mobile.rs`) :

```rust
app.run(|handle, event| match event {
  RunEvent::Opened { urls } => handle_opened_urls(handle, urls), // warm
  RunEvent::Ready => { /* cold: app lancée via fichier, garder splash jusqu'à set_complete */ }
  _ => {}
});
```

- cold : lancement par double-clic sur png/jpg → `Ready` puis `Opened` au démarrage ; on garde `main` hidden jusqu'à `set_complete`/fallback, puis on `show` + `emit("file-opened")`.
- warm : app déjà ouverte → `Opened` seul ; on `show` + `set_focus` + forward au frontend.
