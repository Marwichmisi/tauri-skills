# Opener — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/opener.mdx`, commit `ec113a50`, titre frontmatter `Opener`.

> This plugin allows you to open files and URLs in a specified, or the default, application. It also supports revealing files in the system's file explorer.
>
> Identifiant plugin (frontmatter `plugin:`) : `opener`. Installation : `npm run tauri add opener` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-opener`.

## Usage (fidèle doc)

```js
import { openPath, openUrl } from '@tauri-apps/plugin-opener';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_opener::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `opener:allow-open-url`, `opener:allow-open-path`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Successeur de shell.open (la doc shell renvoie ici pour shell.open).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
