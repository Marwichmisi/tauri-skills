# Store — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/store.mdx`, commit `ec113a50`, titre frontmatter `Store`.

> This plugin provides a persistent key-value store.
>
> Identifiant plugin (frontmatter `plugin:`) : `store`. Installation : `npm run tauri add store` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-store`.

## Usage (fidèle doc)

```js
import { load } from '@tauri-apps/plugin-store';
```

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `store:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Persistant key-value (webview + Rust). Voir state overview dans tauri-ipc-bridge pour alternatives.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
