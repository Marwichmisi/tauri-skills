# OS Information — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/os-info.mdx`, commit `ec113a50`, titre frontmatter `OS Information`.

> Read information about the operating system using the OS Information plugin.
>
> Identifiant plugin (frontmatter `plugin:`) : `os`. Installation : `npm run tauri add os` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-os`.

## Usage (fidèle doc)

```js
import { platform } from '@tauri-apps/plugin-os';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_os::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `os:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Lecture seule (platform, version, arch).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
