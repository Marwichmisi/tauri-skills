# Persisted Scope — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/persisted-scope.mdx`, commit `ec113a50`, titre frontmatter `Persisted Scope`.

> Save filesystem and asset scopes and restore them when the app is reopened.
>
> Identifiant plugin (frontmatter `plugin:`) : `persisted-scope`. Installation : `npm run tauri add persisted-scope` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-persisted-scope`.

## Usage (fidèle doc)

Rust-only : pas de guest-js (`showJsLinks` false dans la fiche). Initialisation Rust : `tauri_plugin_persisted_scope::init()` ; installation `cargo add tauri-plugin-persisted-scope`.

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Forme attendue : `persisted-scope:default` ou `<commande>` documentée ; la liste exacte vit dans la `#permission-table` de la fiche.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Rust-only (showJsLinks false) : sauvegarde/restaure les scopes fs/asset à la réouverture.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
