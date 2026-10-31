# Transcript — eval-command-roundtrip (with_skill)

1. Lu `skills/tauri-ipc-bridge/SKILL.md` (Workflow + Routage : intention commande -> `references/commands.md` + `examples/command-rust.rs` + `examples/command-frontend.js` + `scripts/check-ipc-bridge.py`).
2. Lu `references/commands.md` : `#[tauri::command]`, `invoke_handler/generate_handler`, unicite, `pub` interdit en `lib.rs`, args objet JSON camelCase.
3. Adapte `examples/command-rust.rs` (`my_custom_command` -> `greet(name: String) -> String`) et `examples/command-frontend.js` (`invoke('greet', { name })`).
4. Execute `check-ipc-bridge.py --rust lib.rs --frontend app.js` -> OK.
5. Ecrit `answer.md` avec sources `develop/calling-rust.mdx` commit `ec113a50`.
