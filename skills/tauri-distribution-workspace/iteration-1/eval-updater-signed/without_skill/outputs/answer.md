# Updater Tauri v2 signé — tauri.conf.json

```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "createUpdaterArtifacts": true,
    "windows": {
      "nsis": {
        "installMode": "passive"
      }
    }
  },
  "plugins": {
    "updater": {
      "active": true,
      "dialog": true,
      "endpoints": [
        "https://releases.example.com/{{target}}/{{arch}}/{{current_version}}"
      ],
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6IE1TaXpxYzNWdXZjM1Z3YjI0Z1lXNXBjQT09"
    }
  }
}
```

## Points de validation

- `bundle.createUpdaterArtifacts: true` — génère `.sig` + `latest.json` au `tauri build`.
- `plugins.updater.pubkey` = contenu de la clé publique minisign (commence par `dW50cnVzdGVkIGNvbW1lbnQ6...`), jamais un chemin de fichier.
- `endpoints`: URL `https` uniquement, avec les 3 variables officielles `{{target}}/{{arch}}/{{current_version}}`. Aucune variable inventée (`{{version}}`, `{{platform}}`, etc. interdits).
- `bundle.windows.nsis.installMode: "passive"` — installation silencieuse avec barre de progression sur Windows, requise pour l'updater sans UAC bloquant.
- Prérequis JS : `@tauri-apps/plugin-updater` + `updater` dans `capabilities` (ex. `updater:default`).
