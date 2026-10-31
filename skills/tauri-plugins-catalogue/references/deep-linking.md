# Deep Linking — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/deep-linking.mdx`, commit `ec113a50`, titre frontmatter `Deep Linking`.

> Set your Tauri application as the default handler for an URL.
>
> Identifiant plugin (frontmatter `plugin:`) : `deep-link`. Installation : `npm run tauri add deep-link` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-deep-link@2.0.0`.

## Usage (fidèle doc)

```js
import { getCurrent, onOpenUrl } from '@tauri-apps/plugin-deep-link';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_deep_link::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `deep-link:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Deeplinks (custom scheme / universal links). Voir #permission-table.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
