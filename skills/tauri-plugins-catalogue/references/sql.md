# SQL — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/sql.mdx`, commit `ec113a50`, titre frontmatter `SQL`.

> Plugin providing an interface for the frontend to communicate with SQL databases through sqlx. It supports the SQLite, MySQL and PostgreSQL drivers, enabled by a Cargo feature.
>
> Identifiant plugin (frontmatter `plugin:`) : `sql`. Installation : `npm run tauri add sql` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-sql`.

## Usage (fidèle doc)

```js
import Database from '@tauri-apps/plugin-sql';
```

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `sql:default`, `sql:allow-execute`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Drivers via Cargo feature (sqlite/mysql/postgres).
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
