# Notifications — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/notification.mdx`, commit `ec113a50`, titre frontmatter `Notifications`.

> Send native notifications to your user using the notification plugin.
>
> Identifiant plugin (frontmatter `plugin:`) : `notification`. Installation : `npm run tauri add notification` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-notification`.

## Usage (fidèle doc)

```js
import { isPermissionGranted, requestPermission, sendNotification } from '@tauri-apps/plugin-notification';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_notification::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Forme attendue : `notification:default` ou `<commande>` documentée ; la liste exacte vit dans la `#permission-table` de la fiche.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Voir examples/notification.js (isPermissionGranted/requestPermission/sendNotification, fidèle doc). Permissions : voir #permission-table.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
