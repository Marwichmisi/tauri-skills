# Pipelines + updater — extraits doc

Source: `tauri-docs/src/content/docs/distribute/Pipelines/github.mdx`, commit `ec113a50`, titre frontmatter `GitHub`.
Source: `tauri-docs/src/content/docs/distribute/Pipelines/crabnebula-cloud.mdx`, commit `ec113a50`, titre frontmatter `CrabNebula Cloud`.
Source: `tauri-docs/src/content/docs/distribute/crabnebula-cloud.mdx`, commit `ec113a50`, titre frontmatter `Distributing with CrabNebula Cloud`.
Source: `tauri-docs/src/content/docs/plugin/updater.mdx`, commit `ec113a50`, titre frontmatter `Updater`.
Source: `tauri-docs/src/content/docs/distribute/index.mdx`, commit `ec113a50`, titre frontmatter `Distribute`.

> Automatically update your Tauri app with an update server or a static JSON file (plugin/updater.mdx).
> Tauri's updater needs a signature to verify that the update is from a trusted source. This cannot be disabled.

- Clés : `tauri signer generate -w ~/.tauri/myapp.key` → pubkey (à mettre en `tauri.conf.json`, jamais un chemin) + privée (`TAURI_SIGNING_PRIVATE_KEY`, jamais partagée, perte = plus d'updates pour les installés).
- Build artifacts (`createUpdaterArtifacts`) : `true` (v2) ou `"v1Compatible"` (migration, sera retiré en v3). Linux AppImage (+`.sig`), macOS `.app.tar.gz` (+`.sig`), Windows `.exe`/`.msi` (+`.sig`) en v2 ; `.tar.gz`/`.zip` (+`.sig`) en v1Compatible.
- Config (voir `examples/tauri.conf.updater.json`) :
```json title=tauri.conf.json
{ "bundle": { "createUpdaterArtifacts": true },
  "plugins": { "updater": { "pubkey": "CONTENT FROM PUBLICKEY.PEM",
    "endpoints": ["https://releases.myapp.com/{{target}}/{{arch}}/{{current_version}}"] } } }
```
`endpoints` : tableau d'URLs, TLS exigé en prod, fallback à l'URL suivante si non-2XX. Variables dynamiques seules : `{{current_version}}`, `{{target}}` (`linux/windows/darwin`), `{{arch}}` (`x86_64/i686/aarch64/armv7`). `dangerousInsecureTransportProtocol:true` = http accepté (avec précaution). Windows `installMode` : `passive` (défaut, barre sans interaction), `basicUi` (interaction), `quiet` (sans UI, pas d'admin).
- Pipeline GitHub : `tauri-apps/tauri-action@v1` (voir `examples/publish-github.yml`), matrix macos/ubuntu/windows (+ arm), `tagName: app-v__VERSION__`, signing via secrets (`WINDOWS_CERTIFICATE`, `APPLE_CERTIFICATE`, `TAURI_SIGNING_PRIVATE_KEY`).
- CrabNebula Cloud : distribution + pipeline managés (voir leurs pages), updater pointe vers leurs endpoints.

Valider avec `scripts/check-distribution.py --updater examples/tauri.conf.updater.json`.
