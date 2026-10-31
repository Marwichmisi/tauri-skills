# Pipeline release GitHub — Tauri (baseline, sans skill)

## Tag
`app-v__VERSION__` ex: `app-v0.1.0`. Workflow déclenché sur `push.tags: ["app-v*"]`.

## Matrix
- `macos-latest`, `ubuntu-22.04`, `windows-latest`
- `tauri-apps/tauri-action@v2` build + release en draft.

## Signature
- Updater (tous OS): `TAURI_SIGNING_PRIVATE_KEY` + `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` → génère `.sig` pour updater.
- Windows: `WINDOWS_CERTIFICATE` (base64 pfx) + `WINDOWS_CERTIFICATE_PASSWORD` → signature Authenticode via tauri-action.
- macOS: `APPLE_CERTIFICATE` (base64 p12) + `APPLE_CERTIFICATE_PASSWORD` + `KEYCHAIN_PASSWORD`, + `APPLE_SIGNING_IDENTITY`, notarisation `APPLE_ID` / `APPLE_PASSWORD` / `APPLE_TEAM_ID`.

Secrets à créer dans GitHub → Settings → Secrets → Actions. Ne jamais commiter `signing.env`.

## Fichiers
- `.github/workflows/publish.yml` : voir `publish.yml`
- `signing.env` : template local (non commité), voir `signing.env`
