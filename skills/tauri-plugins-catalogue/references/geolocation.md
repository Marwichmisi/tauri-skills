# Geolocation — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/geolocation.mdx`, commit `ec113a50`, titre frontmatter `Geolocation`.

> Get and track the device's current position, including information about altitude, heading, and speed (if available).
>
> Identifiant plugin (frontmatter `plugin:`) : `geolocation`. Installation : `npm run tauri add geolocation` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-geolocation`.

## Usage (fidèle doc)

```js
import { getCurrentPosition } from '@tauri-apps/plugin-geolocation';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_geolocation::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `geolocation:allow-get-current-position`, `geolocation:allow-watch-position`, `geolocation:allow-check-permissions`, `geolocation:allow-request-permissions`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Voir #permission-table de la fiche.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
