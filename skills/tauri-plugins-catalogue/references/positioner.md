# Positioner — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/positioner.mdx`, commit `ec113a50`, titre frontmatter `Positioner`.

> Position your windows at well-known locations.
>
> Identifiant plugin (frontmatter `plugin:`) : `positioner`. Installation : `npm run tauri add positioner` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-positioner`.

## Usage (fidèle doc)

```js
import { moveWindow, Position } from '@tauri-apps/plugin-positioner';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_positioner::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `positioner:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Positionnement fenêtres (well-known locations).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
