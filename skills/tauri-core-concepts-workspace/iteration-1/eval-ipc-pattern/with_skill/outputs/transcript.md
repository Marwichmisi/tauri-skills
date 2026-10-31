# Transcript (bref)

Références lues (skill `tauri-core-concepts`, commit `ec113a50`) :

1. `SKILL.md` — routage : intention « Choisir Events vs Commands, brownfield vs isolation, écrire le hook et la config `pattern` » → `references/ipc-patterns.md` + exemples `isolation-pattern.json` / `isolation-hook.js`.
2. `references/ipc-patterns.md` (sources : `concept/Inter-Process Communication/index.mdx`, `brownfield.md`, `isolation.md`) — décision isolation : dépendances imbriquées + API Tauri externes ; config, hook, limites (AES-GCM, entropie/haveged, Windows ES Modules, simplicité requise).
3. `references/process-model.md` (source : `concept/process-model.md`) — contexte : logique métier et état global côté Core, moindre privilège.
4. `references/architecture.md` (sources : `concept/architecture.mdx`, `concept/index.mdx`) — contexte vérifié, non déterminant pour le choix.
5. `examples/isolation-pattern.json`, `examples/isolation-hook.js`, `examples/brownfield-pattern.json` — snippets recopiés sans invention (brownfield écarté et justifié).

Sorties écrites dans `outputs/` : `answer.md`, `tauri.conf.json`, `hook.js`, `transcript.md`.
