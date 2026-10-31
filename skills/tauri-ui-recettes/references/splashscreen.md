# Splashscreen — 2 fenêtres, setup frontend+backend, close/show

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/learn/splashscreen.mdx` (titre `Splashscreen`)

> In this lab we'll be implementing a basic splashscreen functionality in a Tauri app. a splashscreen is effectively just a matter of creating a new window that displays some contents during the period your app is doing some heavy setup related tasks and then closing it when setting up is done.

> In general having a splashscreen is an admittance of defeat that you couldn't make your app load fast enough to not need one. it tends to be better to just go straight to a main window that then shows some little spinner somewhere.

## Fenêtres (même fichier)

```json
// src-tauri/tauri.conf.json
{ "windows": [{ "label": "main", "visible": false }, { "label": "splashscreen", "url": "/splashscreen" }] }
```
- `main` cachée (`visible: false`), `splashscreen` affichée (`url: /splashscreen`). Page dédiée (`splashscreen.html` ou route framework, router normal Tauri).

## Setup (même fichier)

- Frontend : `sleep` TS (`setTimeout` promise) puis `invoke('set_complete', {task: 'frontend'})` sur `DOMContentLoaded`.
- Backend : `cargo add tokio -F time` (ne jamais `std::thread::sleep` en async — bloque le runtime coopératif), `spawn(setup(app.handle().clone()))` dans `.setup()` (avant création fenêtres), `sleep(Duration::from_secs(3)).await`.
- État partagé : `struct SetupState { frontend_task: bool, backend_task: bool }` sous `Mutex` via `.manage(...)`, commande `set_complete(app, state, task)` qui, quand les deux flags sont vrais, fait `get_webview_window("splashscreen").close()` + `get_webview_window("main").show()`.

Voir `examples/splashscreen.rs` (extrait fidèle) + `examples/tauri.conf.windows.json`.

Valider avec `scripts/check-ui-recettes.py --config examples/tauri.conf.windows.json --rust examples/splashscreen.rs` (splashscreen sans `main` hidden = FAIL).
