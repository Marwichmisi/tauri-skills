# Events download + Channels

## Rust (`events.rs`)

`app.emit("download-started"/"download-progress"/"download-finished")` (global, `Emitter`). Payloads JSON (`String`/`number`), pas de controle capabilities sur les events.

## Frontend (`listen.js`)

`listen('download-started')` + `listen('download-progress')` avec `await` + `unlisten` au cleanup (`once('download-finished')`). `once` pour ecoute unique.

## Quand passer aux Channels

Events : petits messages, multi-producteur/multi-consommateur (ex notifications). Non adaptes au haut debit/faible latence (eval direct de JS) ni aux gros messages (payloads JSON strings). Channels : rapides, ordonnes, streaming (progress, child process, WebSocket) — `Channel<T>` Rust + `new Channel()` + `onmessage` JS, voir `references/events.md`.

## Scopes

Les events/channels n'ont pas de support du systeme de capabilities : tout scope/permission remonte au skill `tauri-security-capabilities`.

## Sources

- `tauri-docs/src/content/docs/develop/calling-frontend.mdx`, commit `ec113a50`, titre `Calling the Frontend from Rust`.
- `tauri-docs/src/content/docs/develop/_sections/frontend-listen.mdx`, commit `ec113a50`, titre `Calling the Frontend from Rust`.
