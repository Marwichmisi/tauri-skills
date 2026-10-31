# Sidecar + ressource

## Config (`tauri.conf.json`)

`bundle.externalBin: ["binaries/my-sidecar"]` (chemin relatif a `tauri.conf.json`, sans suffixe). `bundle.resources: ["lang/*"]`.

## Binaire par architecture (`rename.js`)

Le binaire sur disque doit porter `-$TARGET_TRIPLE` : `src-tauri/binaries/my-sidecar-x86_64-unknown-linux-gnu` (Linux), `my-sidecar-aarch64-apple-darwin` (macOS). Triple via `rustc --print host-tuple` (Rust 1.84+, sinon parser `rustc -Vv`). Voir `rename.js` (`fs.renameSync`, `.exe` sur win32).

## Resolution ressource

Rust : `app.path().resolve("lang/de.json", BaseDirectory::Resource)` (ou `handle.path()` en commande). JS : `resolveResource('lang/de.json')` (`@tauri-apps/api/path`). Regle `../` -> `_up_`, racine -> `_root_` identique a la config.

## Frontiere securite

`shell:allow-execute` (ou `shell:allow-spawn` pour `spawn()`) avec `{ name: "binaries/my-sidecar", sidecar: true }` + `args` exacts — doctrine detenue par `tauri-security-capabilities`, jamais dupliquee ici. De meme pour `fs:allow-resource-read-recursive` / `$RESOURCE/**/*`.

## Sources

- `tauri-docs/src/content/docs/develop/sidecar.mdx`, commit `ec113a50`, titre `Embedding External Binaries`.
- `tauri-docs/src/content/docs/learn/sidecar-nodejs.mdx`, commit `ec113a50`, titre `Node.js as a sidecar`.
- `tauri-docs/src/content/docs/develop/resources.mdx`, commit `ec113a50`, titre `Embedding Additional Files`.
