# Process — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/process.mdx`, commit `ec113a50`, titre frontmatter `Process`.

> This plugin provides APIs to access the current process. To spawn child processes, see the shell plugin.
>
> Identifiant plugin (frontmatter `plugin:`) : `process`. Installation : `npm run tauri add process` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-process`.

## Usage (fidèle doc)

```js
import { exit, relaunch } from '@tauri-apps/plugin-process';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_process::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `process:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Process courant seul ; spawn/execute vit dans shell (voir fiche shell).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
