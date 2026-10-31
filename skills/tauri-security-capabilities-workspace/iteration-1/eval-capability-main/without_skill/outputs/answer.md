# Capability — fenêtre `main`

Fichier : `capability.json` (à placer dans `src-tauri/capabilities/main-capability.json`)

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window with core defaults plus allow-set-title",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:app:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default",
    "core:window:allow-set-title"
  ]
}
```

## Notes

- `identifier`: `main-capability` — identifiant unique requis par Tauri v2.
- `windows: ["main"]` — restreint cette capability à la fenêtre labellisée `main` (doit correspondre au `label` dans `tauri.conf.json`).
- `core:*:default` — regroupe les permissions par défaut jugées sûres pour chaque plugin core :
  - `core:path:default`, `core:event:default`, `core:window:default`, `core:app:default`, `core:resources:default`, `core:menu:default`, `core:tray:default`.
- `core:window:allow-set-title` — ajout explicite permettant au frontend d'appeler `setTitle` sur la fenêtre `main`, sans ouvrir les autres setters window (minimize, close, set-fullscreen, etc.).
- Principe least-privilege : on ne met pas `core:window:allow-all` ni `*`.
