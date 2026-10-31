# Plugin APIs — 27 guest-js

Sources régénérées avant écriture (commit figé tauri-docs `ec113a50`) :
- `plugins-workspace@df59420 plugins/*/guest-js/index.ts` (27 modules)
- Liste gelée `js-api-generator/build.ts` : autostart, barcode-scanner, biometric,
  cli, clipboard-manager, deep-link, dialog, fs, geolocation, global-shortcut,
  haptics, http, log, nfc, notification, opener, os, positioner, process,
  shell, sql, store, stronghold, updater, upload, websocket, window-state.
- Rust linkée : `https://docs.rs/tauri-plugin-<nom>/2/...`, jamais copiée.
- Régénéré le 2026-10-31 via sparse checkout `df59420`.

Import unique : `import { ... } from '@tauri-apps/plugin-<nom>'`
(package `tauri-plugin-<nom>-api`, scope `@scope/plugin-<nom>` conseillé).
Permissions/scopes : doctrine `tauri-security-capabilities`, jamais inventées.

| Plugin | Import | Fonction phare (source guest-js) |
|---|---|---|
| autostart | `@tauri-apps/plugin-autostart` | `isEnabled/enable/disable` |
| barcode-scanner | `@tauri-apps/plugin-barcode-scanner` | `scan/cancel/checkPermissions` |
| biometric | `@tauri-apps/plugin-biometric` | `checkStatus/authenticate` |
| cli | `@tauri-apps/plugin-cli` | `getMatches` (argv) |
| clipboard-manager | `@tauri-apps/plugin-clipboard-manager` | `writeText/readText` |
| deep-link | `@tauri-apps/plugin-deep-link` | `getCurrent/onOpenUrl` |
| dialog | `@tauri-apps/plugin-dialog` | `open/save/message/ask/confirm` |
| fs | `@tauri-apps/plugin-fs` | `readTextFile/writeTextFile/open/watch` + `BaseDirectory` |
| geolocation | `@tauri-apps/plugin-geolocation` | `getCurrentPosition/watchPosition` |
| global-shortcut | `@tauri-apps/plugin-global-shortcut` | `register/unregister` |
| haptics | `@tauri-apps/plugin-haptics` | `vibrate/impactFeedback` |
| http | `@tauri-apps/plugin-http` | `fetch` (`Client`, `Proxy`) |
| log | `@tauri-apps/plugin-log` | `info/error/attachLogger/attachConsole` |
| nfc | `@tauri-apps/plugin-nfc` | `scan/record` |
| notification | `@tauri-apps/plugin-notification` | `send/isPermissionGranted/requestPermission` |
| opener | `@tauri-apps/plugin-opener` | `openUrl/openPath/revealItemInDir` |
| os | `@tauri-apps/plugin-os` | `platform/arch/version/locale` |
| positioner | `@tauri-apps/plugin-positioner` | `moveWindow/moveWindowConstrained` |
| process | `@tauri-apps/plugin-process` | `exit/relaunch` |
| shell | `@tauri-apps/plugin-shell` | `Command.create/open` (scope `shell:allow-execute`) |
| sql | `@tauri-apps/plugin-sql` | `Database.load/execute/select` |
| store | `@tauri-apps/plugin-store` | `load/Store/LazyStore` |
| stronghold | `@tauri-apps/plugin-stronghold` | `Client/Vault` |
| updater | `@tauri-apps/plugin-updater` | `check/downloadAndInstall` |
| upload | `@tauri-apps/plugin-upload` | `upload` |
| websocket | `@tauri-apps/plugin-websocket` | `Websocket` (`ConnectionConfig`) |
| window-state | `@tauri-apps/plugin-window-state` | `saveFlags/restoreState` (`StateFlags`) |

Exemples fidèles :

```typescript
import { open } from '@tauri-apps/plugin-dialog';
import { readTextFile } from '@tauri-apps/plugin-fs';
const file = await open({ multiple: false, filters: [{ name: 'Text', extensions: ['txt'] }] });
if (typeof file === 'string') await readTextFile(file);
```

```typescript
import { Command } from '@tauri-apps/plugin-shell';
Command.create('run-git-commit', ['commit', '-m', 'msg']);
```

Fiches détaillées par plugin : skill `tauri-plugins-catalogue` (30 fiches :
27 guest-js ci-dessus + `updater` rattaché à `tauri-distribution`,
`localhost` sans guest-js, `index` routeur — voir `docs/TRACABILITE.md`).
Ici on n'expose que l'import + signature JS ; toute `plugin:...` remonte à
`tauri-security-capabilities`. Voir `examples/plugin-dialog-fs.js`.
Check : `python3 scripts/check-frontend-bindings.py --frontend examples/plugin-dialog-fs.js`.
