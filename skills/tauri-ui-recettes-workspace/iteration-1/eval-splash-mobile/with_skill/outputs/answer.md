# Eval 3 — Splashscreen + mobile multi-fenêtres + file associations

Sources (commit `ec113a50`, EN canonique seule) :
- `tauri-docs/src/content/docs/learn/splashscreen.mdx` (titre `Splashscreen`)
- `tauri-docs/src/content/docs/learn/mobile-multiwindow.mdx` (titre `Multi-Window on Mobile`)
- `tauri-docs/src/content/docs/learn/mobile-file-associations.mdx` (titre `File Associations on Mobile`)

Routage skill `tauri-ui-recettes` : `references/splashscreen.md` + `references/mobile.md`,
exemples `examples/tauri.conf.windows.json`, `examples/tauri.conf.file-associations.json`,
`examples/splashscreen.rs`, `examples/mobile-windows.js`, `examples/mobile-windows.rs`.

## 1. Splashscreen — 2 fenêtres

`tauri.conf.json` (`app.windows`) :

```json
{
  "app": {
    "windows": [
      { "label": "main", "visible": false },
      { "label": "splashscreen", "url": "/splashscreen" }
    ]
  }
}
```

- `main` avec `visible: false` (cachée), `splashscreen` affichée avec `url: "/splashscreen"`.
- Page dédiée (`splashscreen.html` ou route framework). Voir `tauri.conf.json` livré.

Frontend splashscreen (`learn/splashscreen.mdx`) : `sleep` TS (`setTimeout` promise)
puis `invoke('set_complete', {task: 'frontend'})` sur `DOMContentLoaded`.

Backend splashscreen (`splashscreen.rs` livré) :
- `cargo add tokio -F time` (ne jamais `std::thread::sleep` en async — bloque le runtime coopératif).
- `struct SetupState { frontend_task: bool, backend_task: bool }` sous `Mutex` via `.manage(...)`.
- `spawn(setup(app.handle().clone()))` dans `.setup()`, `tokio::time::sleep(Duration::from_secs(3)).await`.
- Commande `set_complete(app, state, task)` : quand les deux flags sont vrais,
  `get_webview_window("splashscreen").close()` + `get_webview_window("main").show()`.

```rust
use tokio::time::{sleep, Duration};
struct SetupState { frontend_task: bool, backend_task: bool }
tauri::async_runtime::spawn(setup(app.handle().clone()));
sleep(Duration::from_secs(3)).await;
// puis set_complete(..., "backend") ; frontend via invoke('set_complete', {task:'frontend'})
// complet => get_webview_window("splashscreen").close() + get_webview_window("main").show()
```

## 2. Mobile multi-fenêtres

Capability (`learn/mobile-multiwindow.mdx`, doctrine en `tauri-security-capabilities`) :

```json title="src-tauri/capabilities/default.json"
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main", "main-*"],
  "permissions": ["core:default", "core:webview:allow-create-webview-window"]
}
```

- `core:webview:allow-create-webview-window` requise pour créer des fenêtres dynamiques.
- Fenêtres dynamiques (`main-1`, `main-2`, …) : wildcard `"windows": ["main", "main-*"]`.

JS (`mobile.js` livré) :

```js
import { WebviewWindow } from '@tauri-apps/api/webviewWindow';
const webview = new WebviewWindow(`detail-${id}`, {
  url: `detail/${id}`,
  activityName: 'DetailActivity',
});
webview.once('tauri://created', () => {});
webview.once('tauri://error', (e) => {});
if (await app.supportsMultipleWindows()) {}
```

- `new WebviewWindow(..., { activityName: 'DetailActivity' })` + `once('tauri://created'/'tauri://error')`.
- Android : `activityName` / `createdByActivityName` ; iOS : `requestedBySceneIdentifier`.

Rust (`mobile.rs` livré) :

```rust
// iOS : RunEvent::SceneRequested -> WebviewWindowBuilder main-N
if let tauri::RunEvent::SceneRequested { .. } = event {
    tauri::WebviewWindowBuilder::new(app, format!("main-{counter}"), tauri::WebviewUrl::default()).build().unwrap();
}
// Android : builder.activity_name("DetailActivity")
let builder = tauri::WebviewWindowBuilder::new(main, "detail", tauri::WebviewUrl::App("detail/1".into()));
#[cfg(target_os = "android")]
let builder = builder.activity_name("DetailActivity");
```

- `RunEvent::SceneRequested` exige `WebviewWindowBuilder` (iOS 13+, compteur `cfg(target_os = "ios")`).
- Android : embedding `DetailActivity : TauriActivity()`, `supportsMultipleWindows` à runtime.

## 3. File associations mobile

`tauri.conf.json` (`bundle.fileAssociations`, `ext` sans point) :

```json
{
  "bundle": {
    "fileAssociations": [
      { "ext": ["png"], "mimeType": "image/png" },
      { "ext": ["jpg", "jpeg"], "mimeType": "image/jpeg" }
    ]
  }
}
```

Rust cold+warm (`mobile.rs` livré, `learn/mobile-file-associations.mdx`) :

```rust
struct OpenedUrls(Mutex<Vec<tauri::Url>>);
fn opened_urls(app: tauri::AppHandle) -> Vec<tauri::Url> { /* cold */ }
if let tauri::RunEvent::Opened { urls } = event {
    app.state::<OpenedUrls>().0.lock().unwrap().extend(urls.clone());
    app.emit("opened", urls).unwrap(); // warm
}
```

- `RunEvent::Opened { urls }` (macOS/iOS/Android) : stocker en `OpenedUrls(Mutex<Vec<Url>>>)`
  + commande `opened_urls` (cold) + `app.emit("opened", urls)` (warm).
- Sans `emit("opened")` = FAIL.

JS cold+warm (`mobile.js` livré) :

```js
const initialUrls = await invoke('opened_urls'); // cold
await listen('opened', (event) => { console.log(event.payload); }); // warm
```

- `invoke('opened_urls')` (cold) + `listen('opened')` (warm) exigés ensemble.

## 4. Validation `scripts/check-ui-recettes.py`

```
OK ../tauri-ui-recettes-workspace/iteration-1/eval-splash-mobile/with_skill/outputs/tauri.conf.json
 - windows: ['main', 'splashscreen']
 - fileAssociations: 2 entrée(s)
OK ../tauri-ui-recettes-workspace/iteration-1/eval-splash-mobile/with_skill/outputs/mobile.js
 - frontend APIs: WebviewWindow, activityName, listen, opened_urls, supportsMultipleWindows
OK ../tauri-ui-recettes-workspace/iteration-1/eval-splash-mobile/with_skill/outputs/splashscreen.rs
 - rust APIs: get_webview_window
OK ../tauri-ui-recettes-workspace/iteration-1/eval-splash-mobile/with_skill/outputs/mobile.rs
 - rust APIs: OpenedUrls, RunEvent::Opened, RunEvent::SceneRequested, WebviewWindowBuilder, activity_name, emit("opened", opened_urls
```

Fichiers livrés : `tauri.conf.json`, `splashscreen.rs`, `mobile.js`, `mobile.rs`.
