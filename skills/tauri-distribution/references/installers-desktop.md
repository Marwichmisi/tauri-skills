# Installers desktop Windows/macOS — extraits doc

Source: `tauri-docs/src/content/docs/distribute/windows-installer.mdx`, commit `ec113a50`, titre frontmatter `Windows Installer`.
Source: `tauri-docs/src/content/docs/distribute/dmg.mdx`, commit `ec113a50`, titre frontmatter `DMG`.
Source: `tauri-docs/src/content/docs/distribute/macos-application-bundle.mdx`, commit `ec113a50`, titre frontmatter `macOS Application Bundle`.
Source: `tauri-docs/src/content/docs/distribute/index.mdx`, commit `ec113a50`, titre frontmatter `Distribute`.

> Tauri builds your application directly from its CLI via the `build`, `android build` and `ios build` commands (distribute/index.mdx).
> By default the `build` command automatically bundles your application for the configured formats.

- Windows : `.msi` (WiX v3, Windows-only, exige VBSCRIPT) et NSIS (`.exe`). Build : `tauri build` sur Windows ; sortie `target/x86_64-pc-windows-msvc/release/bundle/nsis/`. WebView2 via `bundle > windows > webviewInstallMode` : `downloadBootstrapper` (défaut, léger), `embedBootstrapper` (~1.8MB, Win7 msi), `offlineInstaller`, `skip`. Exemple doc :
```json title="tauri.conf.json"
{ "bundle": { "windows": { "webviewInstallMode": { "type": "embedBootstrapper" } } } }
```
- macOS : `.app` via `tauri build -- --bundles app`, DMG via `tauri build -- --bundles dmg`. App Store : `tauri bundle -- --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json`.
- Split build/bundle : `tauri build -- --no-bundle` puis `tauri bundle -- --bundles app,dmg`.

Valider avec `scripts/check-distribution.py --bundle examples/tauri.conf.bundle.json`.
