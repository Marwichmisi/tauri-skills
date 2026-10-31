# Transcript — eval invoke-channel (with_skill)

1. Lu `SKILL.md` (routage core → `references/core-api.md`, `examples/invoke-channel.js`, `examples/channel-rust.rs`, check `--frontend` + `--rust`).
2. Lu `references/core-api.md` (sources `tauri@37b3be6 packages/api/src/core.ts`, régénéré 2026-10-31, pin `ec113a50`), `examples/invoke-channel.js`, `examples/channel-rust.rs`.
3. Vérifié sources régénérées `/tmp/opencode/fb-regen/tauri-src/packages/api/src/core.ts` (invoke, Channel, convertFileSrc, docs.rs links).
4. Produit `outputs/invoke-channel.js` (copie fidèle exemple/doc) et `outputs/channel-rust.rs` (lien docs.rs exigé).
5. Lancé `python3 scripts/check-frontend-bindings.py --frontend <js> --rust <rs>` → `OK` core + docs.rs + Channel.
6. Écrit `answer.md` (sources + commandes + sortie OK) et ce `transcript.md`.
