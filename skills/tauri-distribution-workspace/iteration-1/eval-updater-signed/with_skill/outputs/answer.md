# Updater Tauri v2 signé

`tauri.conf.json` :

```json
{
  "bundle": {
    "createUpdaterArtifacts": true
  },
  "plugins": {
    "updater": {
      "pubkey": "dW50cnVzdCBjb21tZW50OiBzaWduIHdpdGggdGF1cmkgdGVzdGtleQ==",
      "endpoints": [
        "https://releases.myapp.com/{{target}}/{{arch}}/{{current_version}}"
      ],
      "windows": {
        "installMode": "passive"
      }
    }
  }
}
```

Notes :
- `bundle.createUpdaterArtifacts: true` (v2).
- `plugins.updater.pubkey` = contenu de la clé (`tauri signer generate`), jamais un chemin.
- `endpoints` https avec `{{target}}/{{arch}}/{{current_version}}` seuls (`target`: linux/windows/darwin, `arch`: x86_64/i686/aarch64/armv7).
- Windows `installMode: passive` (défaut, barre sans interaction).
- Fichier validé : `OK ... updater pubkey + 1 endpoint(s) https` via `scripts/check-distribution.py --updater`.

Sources (EN canonique seule) :
- `tauri-docs/src/content/docs/plugin/updater.mdx`, commit `ec113a50`, titre `Updater`
- `tauri-docs/src/content/docs/distribute/Pipelines/github.mdx`, commit `ec113a50`, titre `GitHub`
