# Stronghold — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/stronghold.mdx`, commit `ec113a50`, titre frontmatter `Stronghold`.

> Store secrets and keys using the IOTA Stronghold secret management engine.
>
> Identifiant plugin (frontmatter `plugin:`) : `stronghold`. Installation : `npm run tauri add stronghold` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-stronghold`.

## Usage (fidèle doc)

```js
import { Client, Stronghold } from '@tauri-apps/plugin-stronghold';
```

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `stronghold:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Secrets/keys chiffrés (IOTA Stronghold).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
