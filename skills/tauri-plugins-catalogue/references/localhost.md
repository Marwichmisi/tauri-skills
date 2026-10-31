# Localhost — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/localhost.mdx`, commit `ec113a50`, titre frontmatter `Localhost`.

> Expose your app's assets through a localhost server instead of the default custom protocol.
>
> Identifiant plugin (frontmatter `plugin:`) : `localhost`. Installation : `npm run tauri add localhost` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-localhost`.

## Usage (fidèle doc)

Rust-only : pas de guest-js (`showJsLinks` false dans la fiche). Initialisation Rust : `voir fiche` ; installation `cargo add tauri-plugin-localhost`.

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Forme attendue : `localhost:default` ou `<commande>` documentée ; la liste exacte vit dans la `#permission-table` de la fiche.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Rust-only (showJsLinks false) : pas de guest-js. Caution doc : considerable security risks, only if you know what you are doing ; en doute, protocole custom par défaut.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
