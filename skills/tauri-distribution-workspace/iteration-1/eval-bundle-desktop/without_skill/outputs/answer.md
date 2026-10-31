# Distribution desktop — Windows + macOS (config unique)

## 1. Windows : MSI + NSIS signé, `webviewInstallMode: embedBootstrapper`

`tauri.conf.json` :
```json
{
  "bundle": {
    "active": true,
    "targets": ["msi", "nsis"],
    "windows": {
      "webviewInstallMode": { "type": "embedBootstrapper" },
      "wix": { "language": "fr-FR" },
      "nsis": { "installerHooks": "src-tauri/nsis-hooks.nsh" }
    }
  }
}
```
`embedBootstrapper` : inclut le bootstrapper WebView2 dans le binaire (~150 Mo). Évite l'échec offline si `downloadBootstrapper` / `offlineInstaller`. Obligatoire pour MSI en entreprise sans internet.

Build :
```bash
rustup target add x86_64-pc-windows-msvc
npm run tauri build -- --target x86_64-pc-windows-msvc --bundles msi,nsis
# sorties : src-tauri/target/x86_64-pc-windows-msvc/release/bundle/{msi/*.msi, nsis/*.exe}
```

Signature (2 niveaux) :
1. Updater Tauri : `TAURI_SIGNING_PRIVATE_KEY` + `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` → `.sig` Minisign.
2. Code-sign Windows (SmartScreen) : `signtool` via `bundle.windows.signCommand` ou `certificateThumbprint`, ou Azure Trusted Signing en CI. Cert EV / OV requis, timestamp `http://timestamp.digicert.com`.

## 2. macOS : app + dmg, `universal-apple-darwin`

`tauri.conf.json` (même fichier, pas de skill par OS) :
```json
{
  "bundle": {
    "macOS": {
      "minimumSystemVersion": "10.15",
      "signingIdentity": "-"
    },
    "dmg": { "background": "src-tauri/dmg-background.png" }
  }
}
```

Build universel :
```bash
rustup target add aarch64-apple-darwin x86_64-apple-darwin
npm run tauri build -- --target universal-apple-darwin --bundles app,dmg
# sorties : src-tauri/target/universal-apple-darwin/release/bundle/{macos/*.app, dmg/*.dmg}
```
`universal-apple-darwin` = lipo aarch64 + x86_64. Requiert Xcode + `rustc` universal. `app` seul pour dev/test local, `dmg` pour distribution.

Signature + notarisation :
```bash
export APPLE_SIGNING_IDENTITY="Developer ID Application: Team (TEAMID)"
export APPLE_CERTIFICATE="..." APPLE_CERTIFICATE_PASSWORD="..."
export APPLE_ID="dev@example.com" APPLE_PASSWORD="app-specific-password" APPLE_TEAM_ID="TEAMID"
```
Tauri `@tauri-apps/plugin-process` / `tauri-cli` signe puis notarise (`notarytool submit --wait`). Sans notarisation : Gatekeeper bloque sur macOS récent.

## 3. Un seul pipeline (pas de skill par OS)

Un seul `tauri.conf.json` avec sections `bundle.windows` + `bundle.macOS` + `bundle.dmg`. Une seule CI matrix :
```yaml
strategy:
  matrix:
    include:
      - os: windows-latest
        args: --target x86_64-pc-windows-msvc --bundles msi,nsis
      - os: macos-latest
        args: --target universal-apple-darwin --bundles app,dmg
run: npm run tauri build -- ${{ matrix.args }}
```
Updater : un seul `latest.json` avec les 3 artefacts (`*-setup.exe`, `*.msi`, `*.dmg`, `*.app.tar.gz`).
