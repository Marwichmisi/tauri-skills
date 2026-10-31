# Transcript — eval-vscode-debug (without_skill)

## Steps taken
1. Lecture consigne : debug VS Code Tauri v2, binaire `src-tauri/target/debug/mon-app`, launch.json dev (lldb, manifest-path `src-tauri/Cargo.toml`, `--no-default-features`, preLaunchTask `ui:dev`) + prod (`--release`, `ui:build`) + tasks.json (`ui:dev` background `yarn dev`, `ui:build` `yarn build`). Aucun fichier d'entrée.
2. Vérification dossier output : `.../without_skill/outputs/` existe.
3. Rédaction `launch.json` de mémoire générale :
   - `version: 0.2.0`, 2 configs `lldb`/`launch`.
   - Dev : `program` debug/mon-app, `cargo.args` build + manifest-path + --no-default-features, `preLaunchTask: ui:dev`.
   - Prod : `program` release/mon-app, `cargo.args` build --release + manifest-path + --no-default-features, `preLaunchTask: ui:build`.
4. Rédaction `tasks.json` :
   - `version: 2.0.0`.
   - `ui:dev` : shell `yarn dev`, `isBackground: true` + problemMatcher background.
   - `ui:build` : shell `yarn build` + `$tsc`.
   - Respect littéral de `yarn` demandé malgré mention `pnpm`.
5. Rédaction `answer.md` : explication prérequis CodeLLDB, emplacement `.vscode/`, usage F5 dev/prod, note pnpm/yarn.
6. Sauvegarde 4 fichiers dans `outputs/` : `answer.md`, `launch.json`, `tasks.json`, `transcript.md`.

## Notes
- Baseline sans skill, connaissances générales uniquement, aucune doc externe consultée.
- Non vérifié par exécution VS Code / cargo (pas de workspace Tauri réel).
