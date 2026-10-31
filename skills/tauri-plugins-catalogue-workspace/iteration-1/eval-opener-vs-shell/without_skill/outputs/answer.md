# Ouvrir une URL (sans skill)

J'ai utilisé shell :

```js
import { Command } from '@tauri-apps/plugin-shell';
await Command.create('open', ['https://tauri.app']).execute();
```

Capability `shell:allow-open`. Check exit 0 : OK shell: capability valide, aucune permission inventée
 - permission shell:allow-open (préfixe shell)
 - js importe @tauri-apps/plugin-shell
