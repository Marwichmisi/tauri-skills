# Baseline sans skill — plugins (mémoire)

```js
import { openDialog } from '@tauri-apps/api/dialog';
import { readFile } from '@tauri-apps/api/fs';

const file = await openDialog({ filters: ['txt'] });
await readFile(file);
```

Test : mock à la main avec `window.__TAURI__ = {}`.

Scopes : mettre `fs:allow-*` dans la capability, ça devrait passer.
