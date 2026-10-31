# Vérifier un fichier (sans skill)

J'ai utilisé le plugin fs.

```js
import { readFile } from '@tauri-apps/plugin-fs';
await readFile('avatar.png');
```

Capability avec `fs:default` + `fs:allow-read`.

Check : exit 0 (permission `fs:allow-read` non documentée dans la fiche).
