# Capability JSON — fenêtre `main`

Fichier : `capability.json` (copie fidèle de `examples/default-capability.json`).

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
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

## Sources citées

- `references/capabilities.md` — extrait doc, `Source: tauri-docs/src/content/docs/security/capabilities.mdx`, commit `ec113a50`, titre frontmatter `Capabilities`. Contient l'exemple canonique `src-tauri/capabilities/default.json` repris tel quel.
- `examples/default-capability.json` — gabarit minimal appliqué sans modification (7 defaults core + `core:window:allow-set-title`).
- `SKILL.md` — Workflow §3-4 + Routage ligne « Définir une capability » ; règle anti-drift : format `plugin:commande:scope`, aucune permission inventée.

## Résultat du check

```
$ python3 scripts/check-capabilities.py <outputs>/capability.json
OK <outputs>/capability.json: identifier=main-capability, permissions=8
 - core:path:default
 - core:event:default
 - core:window:default
 - core:app:default
 - core:resources:default
 - core:menu:default
 - core:tray:default
 - core:window:allow-set-title
```

Exit code 0. Aucune permission inventée : les 8 permissions sont celles de l'exemple canonique doc-locale.
