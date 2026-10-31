# Upload — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/upload.mdx`, commit `ec113a50`, titre frontmatter `Upload`.

> Upload files from disk to a remote server over HTTP. Download files from a remote HTTP server to disk.
>
> Identifiant plugin (frontmatter `plugin:`) : `upload`. Installation : `npm run tauri add upload` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-upload`.

## Usage (fidèle doc)

```js
import { upload } from '@tauri-apps/plugin-upload';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_upload::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `upload:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Upload/download HTTP de fichiers.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
