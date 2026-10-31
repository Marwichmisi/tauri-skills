# Transcript — eval-sidecar-resources (with_skill)

1. Lu `SKILL.md` -> `references/sidecar.md` + `references/resources.md` + `examples/tauri.conf.sidecar.json` + `examples/tauri.conf.resources.json` + `examples/sidecar-rename.js`.
2. Combine `externalBin` + `resources` en un `tauri.conf.json`, copie `rename.js` (triple `rustc --print host-tuple`).
3. Execute `check-ipc-bridge.py --config tauri.conf.json` -> OK.
4. Ecrit `answer.md` : resolve Rust/JS + frontiere `shell:allow-execute` vers `tauri-security-capabilities`, sources `sidecar.mdx` + `sidecar-nodejs.mdx` + `resources.mdx` commit `ec113a50`.
