# Haptics — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/haptics.mdx`, commit `ec113a50`, titre frontmatter `Haptics`.

> Haptic feedback and vibrations on Android and iOS.
>
> Identifiant plugin (frontmatter `plugin:`) : `haptics`. Installation : `npm run tauri add haptics` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-haptics`.

## Usage (fidèle doc)

```js
import { vibrate } from '@tauri-apps/plugin-haptics';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_haptics::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `haptics:allow-vibrate`, `haptics:allow-impact-feedback`, `haptics:allow-notification-feedback`, `haptics:allow-selection-feedback`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Mobile (android/ios).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
