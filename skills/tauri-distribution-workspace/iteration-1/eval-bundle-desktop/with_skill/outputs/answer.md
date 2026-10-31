# Bundle plan desktop — Windows MSI+NSIS signé, macOS app+dmg

Routage unique via manifeste `tauri-distribution` (SKILL.md → `references/installers-desktop.md`), sans skill par OS.

## Config (bundle.json)

- `bundle.targets = ["msi", "nsis", "app", "dmg"]` — targets documentés seuls (doc `distribute/index.mdx`).
- `bundle.windows.webviewInstallMode = { "type": "embedBootstrapper" }` (~1.8MB, requis Win7 MSI).

## CLI

```sh
# Windows (sur runner Windows, WiX v3 + VBSCRIPT requis pour MSI)
tauri build -- --bundles msi,nsis
# sortie: target/x86_64-pc-windows-msvc/release/bundle/nsis/

# macOS (.app puis DMG)
tauri build -- --bundles app
tauri build -- --bundles dmg
# split équivalent:
tauri build -- --no-bundle && tauri bundle -- --bundles app,dmg

# macOS universel (App Store)
tauri bundle -- --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json
```

Signature : via `WINDOWS_CERTIFICATE` / `WINDOWS_CERTIFICATE_PASSWORD` (Windows) et `APPLE_*` (macOS) — voir `references/signing.md`, validé par `--sign`, pas dupliqué ici.

## Sources (commit ec113a50, EN canonique)

- `tauri-docs/src/content/docs/distribute/windows-installer.mdx`, commit `ec113a50`, titre `Windows Installer` — MSI (WiX v3) vs NSIS (.exe), `bundle > windows > webviewInstallMode` (`downloadBootstrapper` défaut / `embedBootstrapper` / `offlineInstaller` / `skip`).
- `tauri-docs/src/content/docs/distribute/dmg.mdx`, commit `ec113a50`, titre `DMG` — DMG via `tauri build -- --bundles dmg`.
- `tauri-docs/src/content/docs/distribute/macos-application-bundle.mdx`, commit `ec113a50`, titre `macOS Application Bundle` — `.app` via `--bundles app`, variante App Store `--target universal-apple-darwin`.
- `tauri-docs/src/content/docs/distribute/index.mdx`, commit `ec113a50`, titre `Distribute` — `build` bundle automatiquement les formats configurés.
