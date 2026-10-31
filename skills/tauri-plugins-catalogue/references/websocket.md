# Websocket — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/websocket.mdx`, commit `ec113a50`, titre frontmatter `Websocket`.

> Open a WebSocket connection using a Rust client in JavaScript.
>
> Identifiant plugin (frontmatter `plugin:`) : `websocket`. Installation : `npm run tauri add websocket` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-websocket`.

## Usage (fidèle doc)

```js
import WebSocket from '@tauri-apps/plugin-websocket';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_websocket::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `websocket:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Client WebSocket Rust exposé en JS.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
