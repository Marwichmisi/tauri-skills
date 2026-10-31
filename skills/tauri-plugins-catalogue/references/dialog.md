# Dialog — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/dialog.mdx`, commit `ec113a50`, titre frontmatter `Dialog`.

> Native system dialogs for opening and saving files along with message dialogs.
>
> Identifiant plugin (frontmatter `plugin:`) : `dialog`. Installation : `npm run tauri add dialog` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-dialog`.

## Usage (fidèle doc)

```js
import { ask } from '@tauri-apps/plugin-dialog';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_dialog::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Forme attendue : `dialog:default` ou `<commande>` documentée ; la liste exacte vit dans la `#permission-table` de la fiche.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Voir examples/dialog.js (ask Yes/No, fidèle doc). Permissions : voir #permission-table de la fiche.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
