# Pipeline release GitHub + signature (Tauri v2)

## Pipeline (`publish.yml`)
- `tauri-apps/tauri-action@v1`, matrix `macos-latest` (aarch64 + x86_64) / `ubuntu-22.04` / `windows-latest`, `tagName: app-v__VERSION__`, `releaseDraft: true`.
- Base reprise de `examples/publish-github.yml`, env étendu avec les secrets de signature.
- Voir `publish.yml` (outputs).

## Signing vars (`signing.env`)
- Updater (tout OS) : `TAURI_SIGNING_PRIVATE_KEY` (+ `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`) — clé via `tauri signer generate -w ~/.tauri/myapp.key`, pubkey en `plugins.updater.pubkey`. Sans signature l'updater refuse la mise à jour.
- macOS : `APPLE_SIGNING_IDENTITY`, `APPLE_CERTIFICATE` (base64 p12), `APPLE_CERTIFICATE_PASSWORD` (+ notarisation `APPLE_ID`/`APPLE_PASSWORD`/`APPLE_TEAM_ID` si store).
- Windows : `WINDOWS_CERTIFICATE` (base64 pfx), `WINDOWS_CERTIFICATE_PASSWORD` — requis contre le warning SmartScreen.
- Check : `OK signing.env: vars=TAURI_SIGNING_PRIVATE_KEY,TAURI_SIGNING_PRIVATE_KEY_PASSWORD,APPLE_SIGNING_IDENTITY,APPLE_CERTIFICATE,APPLE_CERTIFICATE_PASSWORD,WINDOWS_CERTIFICATE,WINDOWS_CERTIFICATE_PASSWORD`
- Check : `OK publish.yml: vars=GITHUB_TOKEN,TAURI_SIGNING_PRIVATE_KEY,TAURI_SIGNING_PRIVATE_KEY_PASSWORD,APPLE_CERTIFICATE,APPLE_CERTIFICATE_PASSWORD,APPLE_SIGNING_IDENTITY,WINDOWS_CERTIFICATE,WINDOWS_CERTIFICATE_PASSWORD`

## Renvoi stores (si besoin)
- App Store / Microsoft Store / Google Play : voir `references/stores.md` (bundle `app` + notarisation Apple, MSIX signé, AAB + `keystore.properties`). Signature ci-dessus reste le prérequis.

## Sources (commit ec113a50, EN canonique seule)
- `distribute/Pipelines/github.mdx` (titre `GitHub`) — tauri-action, matrix, `tagName: app-v__VERSION__`, secrets `WINDOWS_CERTIFICATE`, `APPLE_CERTIFICATE`, `TAURI_SIGNING_PRIVATE_KEY`.
- `distribute/Sign/windows.mdx` (titre `Windows Code Signing`) — pfx base64 via `WINDOWS_CERTIFICATE`, SmartScreen sans signature.
- Compléments : `distribute/Sign/macos.mdx`, `plugin/updater.mdx` via `references/pipelines-updater.md` + `references/signing.md`.
