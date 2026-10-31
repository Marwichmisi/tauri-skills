# Command Line Interface (CLI) — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/cli.mdx`, commit `ec113a50`, titre frontmatter `Command Line Interface (CLI)`.

> Tauri enables your app to have a CLI through clap, a robust command line argument parser.
>
> Identifiant plugin (frontmatter `plugin:`) : `cli`. Installation : `npm run tauri add cli` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-cli`.

## Usage (fidèle doc)

```js
import { getMatches } from '@tauri-apps/plugin-cli';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_cli::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `cli:default`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Homonyme : ici usage in-app (getMatches) ; la CLI dev (tauri init/dev/build) vit dans tauri-config-cli-reference.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
