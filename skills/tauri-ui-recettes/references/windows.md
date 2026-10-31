# Fenêtres — custom titlebar, decorations, drag, transparent macOS

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/learn/window-customization.mdx` (titre `Window Customization`)

> Tauri provides lots of options for customizing the look and feel of your app's window. You can create custom titlebars, have transparent windows, enforce size constraints, and more.

## Configurer (même fichier)

> There are three ways to change the window configuration: Through tauri.conf.json, Through the JavaScript API, Through the Window in Rust (docs.rs `tauri/window/struct.Window.html`, linkée jamais copiée).

- `tauri.conf.json` (chemin réel `app.windows` ; extrait doc simplifié `tauri.windows`, accepté par le check pour compat) : `decorations: false` pour custom titlebar :
```json title="tauri.conf.json"
{ "tauri": { "windows": [{ "decorations": false }] } }
```

## Titlebar custom (même fichier)

- Capability exigée côté app (doctrine en `tauri-security-capabilities`) :
```json title="src-tauri/capabilities/default.json"
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    "core:window:default",
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-toggle-maximize",
    "core:window:allow-start-dragging"
  ]
}
```
Permissions doc seules (`allow-internal-toggle-maximize` inclus dans `default`).

- HTML : `<div data-tauri-drag-region></div>` sur l'élément exact (les enfants exigent l'attribut chacun, sinon boutons/inputs cassés). Touch/pen Windows : `*[data-tauri-drag-region] { app-region: drag; }`.
- JS : `getCurrentWindow()` puis `minimize()` / `toggleMaximize()` / `close()` (voir `examples/titlebar.js`). Variante manuelle : `mousedown` + `e.buttons === 1` → `toggleMaximize()` si `detail === 2` sinon `startDragging()`.

## macOS transparent (même fichier)

- Retirer la fenêtre de `tauri.conf.json`, créer via `WebviewWindowBuilder::new(app, "main", WebviewUrl::default())` + `.title_bar_style(TitleBarStyle::Transparent)` sous `cfg(target_os = "macos")`, fond via `objc2-app-kit` (`NSWindow::setBackgroundColor`). Dépendance doc : `objc2-app-kit = { version = "0.3.2", features = ["NSColor", "NSWindow", "objc2-core-foundation"] }` sous `[target."cfg(target_os = \"macos\")".dependencies]`.

Valider avec `scripts/check-ui-recettes.py --config examples/tauri.conf.windows.json --frontend examples/titlebar.js`. Labels uniques, `visible`/`decorations` booléens.
