# Shell — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/shell.mdx`, commit `ec113a50`, titre frontmatter `Shell`.

> Access the system shell. Allows you to spawn child processes.
>
> Identifiant plugin (frontmatter `plugin:`) : `shell`. Installation : `npm run tauri add shell` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-shell`.

## Usage (fidèle doc)

```js
import { Command } from '@tauri-apps/plugin-shell';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_shell::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `shell:allow-execute`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Pour shell.open, voir opener (la doc shell renvoie à opener). Scopes shell côté capability exigés.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
