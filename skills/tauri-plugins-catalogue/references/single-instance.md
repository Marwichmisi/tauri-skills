# Single Instance — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/single-instance.mdx`, commit `ec113a50`, titre frontmatter `Single Instance`.

> Ensure that a single instance of your tauri app is running at a time using the Single Instance Plugin.
>
> Identifiant plugin (frontmatter `plugin:`) : `single-instance`. Installation : `npm run tauri add single-instance` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-single-instance`.

## Usage (fidèle doc)

Rust-only : pas de guest-js (`showJsLinks` false dans la fiche). Initialisation Rust : `tauri_plugin_single_instance::init(|app, args, cwd| {})` ; installation `cargo add tauri-plugin-single-instance`.

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Forme attendue : `single-instance:default` ou `<commande>` documentée ; la liste exacte vit dans la `#permission-table` de la fiche.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Rust-only (showJsLinks false) : init(|app, args, cwd|) desktop ; permissions snap/flatpak décrites dans la fiche.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
