# Biometric — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/biometric.mdx`, commit `ec113a50`, titre frontmatter `Biometric`.

> Prompt the user for biometric authentication on Android and iOS.
>
> Identifiant plugin (frontmatter `plugin:`) : `biometric`. Installation : `npm run tauri add biometric` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-biometric`.

## Usage (fidèle doc)

```js
import { checkStatus } from '@tauri-apps/plugin-biometric';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_biometric::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `biometric:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Mobile (android/ios). Voir #permission-table de la fiche.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
