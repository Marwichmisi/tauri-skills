# NFC — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/nfc.mdx`, commit `ec113a50`, titre frontmatter `NFC`.

> Read and write NFC tags on Android and iOS.
>
> Identifiant plugin (frontmatter `plugin:`) : `nfc`. Installation : `npm run tauri add nfc` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-nfc`.

## Usage (fidèle doc)

```js
import { isAvailable } from '@tauri-apps/plugin-nfc';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_nfc::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `nfc:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Mobile (android/ios).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
