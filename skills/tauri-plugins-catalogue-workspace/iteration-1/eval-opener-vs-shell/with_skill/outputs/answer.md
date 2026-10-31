# Fiche opener — routage en une étape (pas shell)

Routage : intention ouvrir URL externe → `references/opener.md` (une étape). `shell.open` exclu : la fiche `plugin/shell.mdx` renvoie à opener (`If you're looking for documentation for the shell.open API, check out the new Opener plugin`).

## Setup (fidèle doc)

```
npm run tauri add opener
cargo add tauri-plugin-opener
```

Rust : `.plugin(tauri_plugin_opener::init())`.

## Snippet (`outputs/opener.js`, fidèle fiche)

```js
import { openUrl } from '@tauri-apps/plugin-opener';
await openUrl('https://tauri.app');
```

## Capability (`outputs/capability.json`)

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability opener",
  "windows": [
    "main"
  ],
  "permissions": [
    "opener:allow-open-url"
  ]
}
```

Doctrine : `#permission-table` de la fiche, `tauri-security-capabilities` pour scopes.

## Sources

- `references/opener.md` — `Source: tauri-docs/src/content/docs/plugin/opener.mdx`, commit `ec113a50`, titre `Opener`.
- `references/shell.md` — renvoi `shell.open` → opener cité.

## Check

```
$ python3 scripts/check-catalogue.py --plugin opener --js outputs/opener.js --capability outputs/capability.json
OK opener: capability valide, aucune permission inventée
 - permission opener:allow-open-url (préfixe opener)
 - js importe @tauri-apps/plugin-opener
```

Exit code 0. Aucune permission inventée : `opener:allow-open-url` cité dans la fiche.
