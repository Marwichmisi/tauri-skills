# Clipboard — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/clipboard.mdx`, commit `ec113a50`, titre frontmatter `Clipboard`.

> Read and write to the system clipboard using the clipboard plugin.
>
> Identifiant plugin (frontmatter `plugin:`) : `clipboard-manager`. Installation : `npm run tauri add clipboard-manager` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-clipboard-manager`.

## Usage (fidèle doc)

```js
import { writeText, readText } from '@tauri-apps/plugin-clipboard-manager';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_clipboard_manager::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Forme attendue : `clipboard-manager:default` ou `<commande>` documentée ; la liste exacte vit dans la `#permission-table` de la fiche.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Préfixe permission = clipboard-manager (frontmatter plugin). Voir #permission-table de la fiche.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
