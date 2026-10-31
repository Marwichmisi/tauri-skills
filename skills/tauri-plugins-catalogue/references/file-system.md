# File System — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/file-system.mdx`, commit `ec113a50`, titre frontmatter `File System`.

> Access the file system.
>
> Identifiant plugin (frontmatter `plugin:`) : `fs`. Installation : `npm run tauri add fs` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-fs`.

## Usage (fidèle doc)

```js
import { exists, BaseDirectory } from '@tauri-apps/plugin-fs';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_fs::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `fs:default`, `fs:allow-exists`, `fs:scope`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Note doc : utiliser std::fs/tokio::fs côté Rust. fs exige scope (allow) en plus de la permission, sinon forbidden path. Exemple : examples/fs.js.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
