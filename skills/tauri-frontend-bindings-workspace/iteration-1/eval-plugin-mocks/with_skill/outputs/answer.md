# Plugins + mocks — réponse

Sources : `plugins-workspace@df59420 plugins/dialog/guest-js/index.ts`
(`open/save/message/ask/confirm`), `plugins/fs/guest-js/index.ts`
(`readTextFile`, `BaseDirectory`), `tauri@37b3be6 packages/api/src/mocks.ts`
(`mockIPC/clearMocks`), régénérés le 2026-10-31, pin `tauri-docs ec113a50`.
Routage : `references/plugin-apis.md` + `references/core-api.md` → `examples/plugin-dialog-fs.js` + `examples/mocks.js`.

## 1. Dialogue + fs (copie fidèle)

`outputs/plugin-dialog-fs.js` :

```js
import { open } from '@tauri-apps/plugin-dialog';
import { readTextFile } from '@tauri-apps/plugin-fs';
const file = await open({ multiple: false, filters: [{ name: 'Text', extensions: ['txt'] }] });
if (typeof file === 'string') await readTextFile(file);
```

Scope `fs` (`$APPDATA/**`, `deny` gagne) : doctrine `tauri-security-capabilities`
(`security/scope.mdx`), jamais inventée ici.

## 2. Test Vitest (copie fidèle `mocks.ts`)

`outputs/mocks.js` :

```js
import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { invoke } from '@tauri-apps/api/core';
mockIPC((cmd, args) => { if (cmd === 'greet') return `Hello, ${args.name}!`; });
await invoke('greet', { name: 'tauri' });
clearMocks();
```

`withGlobalTauri` (`window.__TAURI__`) : config `tauri-start`
(`start/frontend/*`), schéma complet `tauri-config-cli-reference`.

## 3. Validation

```
python3 scripts/check-frontend-bindings.py --frontend outputs/plugin-dialog-fs.js
OK plugin imports: ['dialog', 'fs']
python3 scripts/check-frontend-bindings.py --frontend outputs/mocks.js
OK core imports: ['core', 'mocks']
```
