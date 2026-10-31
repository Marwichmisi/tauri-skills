# Transcript — eval-vscode-debug (with_skill)

## Étapes

1. Lu `skills/tauri-dev-quality/SKILL.md` (routage : intention IDE debug → `references/ide-debug.md`, exemple `examples/launch.json` + `examples/tasks.json`, script `--vscode`).
2. Lu `skills/tauri-dev-quality/references/ide-debug.md` (sections VS Code lldb toutes plateformes + variante Windows cppvsdbg, principe contournement CLI, `preLaunchTask` / serveur dev à part / `--no-default-features`).
3. Lu `skills/tauri-dev-quality/examples/launch.json` (2 configs lldb, dev `--manifest-path=./src-tauri/Cargo.toml --no-default-features` + `preLaunchTask ui:dev`, prod `--release --manifest-path` + `preLaunchTask ui:build`).
4. Lu `skills/tauri-dev-quality/examples/tasks.json` (`ui:dev` shell `yarn dev` + `isBackground true`, `ui:build` shell `yarn build`).
5. Lu `skills/tauri-dev-quality/scripts/check-dev-quality.py` (règles `--vscode` : version `0.2.0`, types `lldb`/`cppvsdbg` seuls, manifest-path ou program src-tauri, `preLaunchTask`, `--no-default-features` dev / `--release` prod).
6. Créé le dossier `skills/tauri-dev-quality-workspace/iteration-1/eval-vscode-debug/with_skill/outputs/`.
7. Écrit `outputs/launch.json` (copie exacte de l'exemple doc) et `outputs/tasks.json` (copie exacte de l'exemple doc).
8. Exécuté `python3 scripts/check-dev-quality.py --vscode outputs/launch.json` → `OK ... launch.json fidèle (2 configs)`, `exit=0`.
9. Écrit `outputs/answer.md` (explication + check output + sources fichier + commit + titre) et le présent `transcript.md`.

## Fichiers lus

- `skills/tauri-dev-quality/SKILL.md`
- `skills/tauri-dev-quality/references/ide-debug.md`
- `skills/tauri-dev-quality/examples/launch.json`
- `skills/tauri-dev-quality/examples/tasks.json`
- `skills/tauri-dev-quality/scripts/check-dev-quality.py`

## Checks run

- `python3 /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-dev-quality/scripts/check-dev-quality.py --vscode /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-dev-quality-workspace/iteration-1/eval-vscode-debug/with_skill/outputs/launch.json` → OK (2 configs), exit 0.
