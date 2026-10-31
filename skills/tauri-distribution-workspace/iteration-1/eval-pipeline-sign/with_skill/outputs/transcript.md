# Transcript — eval 3 pipeline-sign (with skill)

## Steps
1. Lu `skills/tauri-distribution/SKILL.md` → routage : Pipeline + updater = `references/pipelines-updater.md` + `examples/publish-github.yml` ; Signer par OS = `references/signing.md` + `examples/signing.env`.
2. Lu `references/pipelines-updater.md` (Source `distribute/Pipelines/github.mdx`, commit ec113a50) : tauri-action@v1, matrix macos/ubuntu/windows, `tagName: app-v__VERSION__`, secrets signing.
3. Lu `references/signing.md` (Source `distribute/Sign/windows.mdx` + `macos.mdx`, commit ec113a50) : `WINDOWS_CERTIFICATE` (base64 pfx), `APPLE_CERTIFICATE` (base64 p12), `TAURI_SIGNING_PRIVATE_KEY` updater.
4. Lu `references/stores.md` pour le renvoi stores (App Store / Microsoft Store / Google Play).
5. Écrit `signing.env` (7 vars allowlist) + `publish.yml` (exemple + env secrets) dans outputs/.
6. Validé avec `scripts/check-distribution.py --sign`.

## Check output
```
$ python3 skills/tauri-distribution/scripts/check-distribution.py --sign skills/tauri-distribution-workspace/iteration-1/eval-pipeline-sign/with_skill/outputs/signing.env
OK skills/tauri-distribution-workspace/iteration-1/eval-pipeline-sign/with_skill/outputs/signing.env: vars=TAURI_SIGNING_PRIVATE_KEY,TAURI_SIGNING_PRIVATE_KEY_PASSWORD,APPLE_SIGNING_IDENTITY,APPLE_CERTIFICATE,APPLE_CERTIFICATE_PASSWORD,WINDOWS_CERTIFICATE,WINDOWS_CERTIFICATE_PASSWORD

$ python3 skills/tauri-distribution/scripts/check-distribution.py --sign skills/tauri-distribution-workspace/iteration-1/eval-pipeline-sign/with_skill/outputs/publish.yml
OK skills/tauri-distribution-workspace/iteration-1/eval-pipeline-sign/with_skill/outputs/publish.yml: vars=GITHUB_TOKEN,TAURI_SIGNING_PRIVATE_KEY,TAURI_SIGNING_PRIVATE_KEY_PASSWORD,APPLE_CERTIFICATE,APPLE_CERTIFICATE_PASSWORD,APPLE_SIGNING_IDENTITY,WINDOWS_CERTIFICATE,WINDOWS_CERTIFICATE_PASSWORD
```
Exit 0 dans les deux cas. Aucune var inventée.
