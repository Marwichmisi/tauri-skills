# Autostart — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/autostart.mdx`, commit `ec113a50`, titre frontmatter `Autostart`.

> Automatically launch your application at system startup.
>
> Identifiant plugin (frontmatter `plugin:`) : `autostart`. Installation : `npm run tauri add autostart` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-autostart`.

## Usage (fidèle doc)

```js
import { enable, isEnabled, disable } from '@tauri-apps/plugin-autostart';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_autostart::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `autostart:allow-enable`, `autostart:allow-disable`, `autostart:allow-is-enabled`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Desktop seul (macos/windows/linux).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
