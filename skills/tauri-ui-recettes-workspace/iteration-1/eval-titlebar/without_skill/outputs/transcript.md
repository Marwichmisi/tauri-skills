# Transcript — eval titlebar (baseline, sans skill)

- Config `tauri.conf.json` avec `decorations: false` sur window `main`.
- Capability `core:window:*` : default, allow-close, allow-minimize, allow-toggle-maximize, allow-start-dragging.
- HTML avec `data-tauri-drag-region` + CSS `app-region: drag` / `no-drag` sur boutons.
- JS `getCurrentWindow()` avec `minimize()`, `toggleMaximize()`, `close()`.

Outputs : answer.md, tauri.conf.json, titlebar.js.
