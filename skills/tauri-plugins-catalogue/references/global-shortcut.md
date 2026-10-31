# Global Shortcut — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/global-shortcut.mdx`, commit `ec113a50`, titre frontmatter `Global Shortcut`.

> Register global shortcuts.
>
> Identifiant plugin (frontmatter `plugin:`) : `global-shortcut`. Installation : `npm run tauri add global-shortcut` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-global-shortcut`.

## Usage (fidèle doc)

```js
import { register } from '@tauri-apps/plugin-global-shortcut';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_global_shortcut::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `global-shortcut:allow-register`, `global-shortcut:allow-unregister`, `global-shortcut:allow-is-registered`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Raccourcis globaux desktop.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
