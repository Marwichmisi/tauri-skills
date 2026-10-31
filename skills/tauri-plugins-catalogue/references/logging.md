# Logging — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/logging.mdx`, commit `ec113a50`, titre frontmatter `Logging`.

> Configurable logging for your Tauri app.
>
> Identifiant plugin (frontmatter `plugin:`) : `log`. Installation : `npm run tauri add log` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-log`.

## Usage (fidèle doc)

```js
import { info } from '@tauri-apps/plugin-log';
```

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `log:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Init Rust via Builder (.plugin + log::Builder). Voir #permission-table.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
