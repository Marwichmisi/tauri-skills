# HTTP Client — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/http-client.mdx`, commit `ec113a50`, titre frontmatter `HTTP Client`.

> Make HTTP requests with the http plugin.
>
> Identifiant plugin (frontmatter `plugin:`) : `http`. Installation : `npm run tauri add http` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-http`.

## Usage (fidèle doc)

```js
import { fetch } from '@tauri-apps/plugin-http';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_http::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `http:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Client HTTP Rust exposé au frontend.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
