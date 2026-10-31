# Window State — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/window-state.mdx`, commit `ec113a50`, titre frontmatter `Window State`.

> Save window positions and sizes and restore them when the app is reopened.
>
> Identifiant plugin (frontmatter `plugin:`) : `window-state`. Installation : `npm run tauri add window-state` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-window-state`.

## Usage (fidèle doc)

```js
import { saveWindowState, StateFlags } from '@tauri-apps/plugin-window-state';
```

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `window-state:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Persiste taille/position fenêtres.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
