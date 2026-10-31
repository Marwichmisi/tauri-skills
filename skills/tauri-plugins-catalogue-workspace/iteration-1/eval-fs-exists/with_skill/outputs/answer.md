# Fiche file-system — routage en une étape

Routage : intention vérifier existence fichier `$APPDATA/avatar.png` → `references/file-system.md` (une étape, tableau SKILL.md ligne filesystem).

## Setup (fidèle doc)

```
npm run tauri add fs
cargo add tauri-plugin-fs
```

Rust (`lib.rs`) : `.plugin(tauri_plugin_fs::init())`.

## Snippet JS (fidèle `plugin/file-system.mdx`, voir `outputs/fs.js`)

```js
import { exists, BaseDirectory } from '@tauri-apps/plugin-fs';
await exists('avatar.png', { baseDir: BaseDirectory.AppData });
```

## Capability (`outputs/capability.json`)

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window (fs example)",
  "windows": ["main"],
  "permissions": ["fs:default", "fs:allow-exists"]
}
```

Note doc : `fs` exige un scope `allow` en plus de la permission, sinon `forbidden path` à l'exécution (voir fiche). Doctrine scopes/permissions : `tauri-security-capabilities`.

## Sources

- `references/file-system.md` — extrait doc, `Source: tauri-docs/src/content/docs/plugin/file-system.mdx`, commit `ec113a50`, titre `File System`.
- `examples/fs.js` + `examples/capability-fs.json` appliqués sans modification.

## Check

```
$ python3 scripts/check-catalogue.py --plugin file-system --js outputs/fs.js --capability outputs/capability.json
OK file-system: capability valide, aucune permission inventée
 - permission fs:default (préfixe fs)
 - permission fs:allow-exists (préfixe fs)
 - js importe @tauri-apps/plugin-fs
```

Exit code 0. Aucune permission inventée : `fs:default`, `fs:allow-exists` cités dans la fiche.
