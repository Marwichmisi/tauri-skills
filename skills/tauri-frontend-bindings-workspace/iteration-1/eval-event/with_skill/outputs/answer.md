# Events — réponse

Sources : `tauri@37b3be6 packages/api/src/event.ts` (`listen`/`once`/`emit`/`emitTo`, `TauriEvent`),
régénéré le 2026-10-31, pin `tauri-docs ec113a50`.
Routage skill : `references/event-api.md` → `examples/event-listen.js`.

## 1. Frontend JS (copie fidèle doc)

`outputs/event-listen.js` :

```js
import { listen, emit, TauriEvent } from '@tauri-apps/api/event';

const unlisten = await listen(TauriEvent.WINDOW_DESTROYED, (event) => {
  console.log('a window was destroyed', event.payload);
});

await emit('frontend-loaded', { loggedIn: true, token: 'authToken' });
```

Cleanup : appeler `unlisten()` quand le composant se démonte (anti-leak).
Gros volumes ordonnés/rapides → `Channel` (`references/core-api.md`), pas `emit` JSON.

## 2. Validation

```
python3 scripts/check-frontend-bindings.py --frontend outputs/event-listen.js
OK outputs/event-listen.js
 - core imports: ['event']
```

`core:event:default` actif par défaut (`allow-listen/unlisten/emit/emit-to`),
aucune capability supplémentaire. Scopes éventuels → `tauri-security-capabilities`.
