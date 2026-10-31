# Barcode Scanner — fiche catalogue

Source: `tauri-docs/src/content/docs/plugin/barcode-scanner.mdx`, commit `ec113a50`, titre frontmatter `Barcode Scanner`.

> Allows your mobile application to use the camera to scan QR codes, EAN-13 and other kinds of barcodes.
>
> Identifiant plugin (frontmatter `plugin:`) : `barcode-scanner`. Installation : `npm run tauri add barcode-scanner` (doc, onglet Automatic) ; manuel `src-tauri` : `cargo add tauri-plugin-barcode-scanner`.

## Usage (fidèle doc)

```js
import { scan, Format } from '@tauri-apps/plugin-barcode-scanner';
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_barcode_scanner::init())` (doc, onglet Manual).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table` (composant `PluginPermissions` de la fiche). Référence-les dans une capability, n'invente jamais de permission.

Exemples fidèles cités dans la fiche : `barcode-scanner:allow-scan`, `barcode-scanner:allow-cancel`.

Doctrine : toute question de permission/scope/capability se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`), pas ici.

## Notes

- Mobile (android/ios) : scan via caméra.
- `plugin/updater.mdx` exclu du catalogue (vit dans `tauri-distribution`, voir `references/pipelines-updater.md`).
