# Transcript — eval-events-channels (with_skill)

1. Lu `SKILL.md` -> `references/events.md` + `examples/event-rust.rs` + `examples/event-frontend.js`.
2. Repris `emit("download-started"/"download-progress")` Rust et `listen` frontend avec `await` + `unlisten`/`once`.
3. Execute `check-ipc-bridge.py --rust events.rs --frontend listen.js` -> OK (event commun `download-started`).
4. Ecrit `answer.md` : regle channels (ordonnes/streaming) + renvoi scopes vers `tauri-security-capabilities`, sources `calling-frontend.mdx` + `frontend-listen.mdx` commit `ec113a50`.
