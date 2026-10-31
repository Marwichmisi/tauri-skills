# Event API — listen, once, emit, emitTo, TauriEvent

Sources régénérées avant écriture (commit figé tauri-docs `ec113a50`) :
- `tauri@37b3be6 packages/api/src/event.ts`
  (`@module` event system, `@remarks` permission `core:event:default`)
- Rust linkée : `https://docs.rs/tauri/2/tauri/struct.AppHandle.html#method.listen`
  (côté Rust `app.listen`), jamais copiée.
- Régénéré le 2026-10-31 via sparse checkout `37b3be6`.

> The event system allows you to emit events to the backend and listen to events from it.
> This package is also accessible with `window.__TAURI__.event` when
> `app.withGlobalTauri` in `tauri.conf.json` is set to `true`.
> All commands used by this module are part of the `core:event:default`
> permission set, enabled by default, so no extra capability configuration is needed.

## listen / once

```typescript
async function listen<T>(
  event: string,
  handler: EventCallback<T>,
  options?: Options
): Promise<UnlistenFn>
async function once<T>(event: string, handler: EventCallback<T>): Promise<UnlistenFn>
```

`Options.target` : `{ kind: 'Any' }` (défaut), `{ kind: 'AnyLabel', label }`,
`{ kind: 'App' }`, `{ kind: 'Window'|'Webview'|'WebviewWindow', label }`.
String = `AnyLabel`. Retour `UnlistenFn` à appeler (cleanup, anti-leak).

## emit / emitTo

```typescript
async function emit<T>(event: string, payload?: T): Promise<void>
async function emitTo<T>(target: EventTarget | string, event: string, payload?: T): Promise<void>
```

> ```typescript
> import { emit } from '@tauri-apps/api/event';
> await emit('frontend-loaded', { loggedIn: true, token: 'authToken' });
> ```

Noms : alphanum + `-`, `/`, `:`, `_` seuls (`tauri://...` inclus).
Check rejette `bad event!`. Gros volumes ordonnés/rapides : `Channel`
(voir `references/core-api.md`), pas `emit` JSON.

## TauriEvent

```typescript
enum TauriEvent {
  WINDOW_RESIZED = 'tauri://resize',
  WINDOW_MOVED = 'tauri://move',
  WINDOW_CLOSE_REQUESTED = 'tauri://close-requested',
  WINDOW_DESTROYED = 'tauri://destroyed',
  WINDOW_FOCUS = 'tauri://focus',
  WINDOW_BLUR = 'tauri://blur',
  WINDOW_SCALE_FACTOR_CHANGED = 'tauri://scale-change',
  WINDOW_THEME_CHANGED = 'tauri://theme-changed',
  WINDOW_CREATED = 'tauri://window-created',
  // ...
}
```

> ```typescript
> import { listen, TauriEvent } from '@tauri-apps/api/event';
> const unlisten = await listen(TauriEvent.WINDOW_DESTROYED, (event) => {
>   console.log('a window was destroyed', event.payload);
> });
> ```

Préférer helpers `Window.onResized`/`onMoved`/etc quand ils existent
(payload décodé `PhysicalSize`/`PhysicalPosition`). Voir `references/app-path-window.md`.

Exemple minimal : `examples/event-listen.js`.
Check : `python3 scripts/check-frontend-bindings.py --frontend examples/event-listen.js`.
