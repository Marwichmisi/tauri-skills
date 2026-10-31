# Frontends Rust (Leptos/Trunk) — extraits doc

Commit `ec113a50`, EN canonique. SSG seuls, pas de serveur (voir `frontend-vite.md`).

## Leptos

Source : `tauri-docs/src/content/docs/start/frontend/leptos.mdx` (titre `Leptos`, exact à Leptos 0.6).

> Leptos is a Rust based web framework.

Checklist (même fichier) :
- Use SSG, Tauri doesn't officially support server based solutions.
- Use `serve.ws_protocol = "ws"` so that the hot-reload websocket can connect properly for mobile development.
- Enable `withGlobalTauri` to ensure that Tauri APIs are available in the `window.__TAURI__` variable and can be imported using `wasm-bindgen`.

Config Tauri — voir `examples/tauri.conf.leptos.json` (copie exacte) :

```json
{
  "build": { "beforeDevCommand": "trunk serve", "devUrl": "http://localhost:1420", "beforeBuildCommand": "trunk build", "frontendDist": "../dist" },
  "app": { "withGlobalTauri": true }
}
```

Config Trunk (même fichier) :

```toml
[build]
target = "./index.html"
[watch]
ignore = ["./src-tauri"]
[serve]
port = 1420
open = false
ws_protocol = "ws"
```

## Trunk

Source : `tauri-docs/src/content/docs/start/frontend/trunk.mdx` (titre `Trunk`, exact à Trunk 0.17.5).

> Trunk is a WASM web application bundler for Rust.

Checklist (même fichier) : identique à Leptos (SSG, `ws_protocol = "ws"`, `withGlobalTauri`).

Config Tauri — voir `examples/tauri.conf.trunk.json` (copie exacte) :

```json
{
  "build": { "beforeDevCommand": "trunk serve", "beforeBuildCommand": "trunk build", "devUrl": "http://localhost:8080", "frontendDist": "../dist" },
  "app": { "withGlobalTauri": true }
}
```

Config Trunk (même fichier) :

```toml
[watch]
ignore = ["./src-tauri"]
[serve]
ws_protocol = "ws"
```

Le check exige `withGlobalTauri: true` pour `--frontend leptos|trunk`, sinon FAIL.
