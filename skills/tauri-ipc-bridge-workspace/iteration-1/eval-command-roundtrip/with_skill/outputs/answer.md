# Command roundtrip : `greet`

## Rust (`lib.rs`, meme dossier)

`#[tauri::command] fn greet(name: String) -> String` + `invoke_handler(tauri::generate_handler![greet])`. Noms uniques, pas de `pub` dans `lib.rs` (limitation glue code).

## Frontend (`app.js`, meme dossier)

`invoke('greet', { name: 'Tauri' })` — args en objet JSON camelCase (`name` identique des deux cotes).

## Validation

`python3 scripts/check-ipc-bridge.py --rust lib.rs --frontend app.js` -> OK (voir transcript).

## Sources

- `tauri-docs/src/content/docs/develop/calling-rust.mdx`, commit `ec113a50`, titre `Calling Rust from the Frontend` (relayes par `references/commands.md`).
- Aucun contenu invente : `greet` suit le pattern `my_custom_command` documente.
