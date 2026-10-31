# Debug VS Code — app Tauri v2 (`mon-app`)

## Ce qui a été produit

- `launch.json` : 2 configs `lldb` (extension `vscode-lldb`), copies fidèles de `examples/launch.json`.
  - `Tauri Development Debug` : `cargo.args = build --manifest-path=./src-tauri/Cargo.toml --no-default-features`, `preLaunchTask: ui:dev`.
  - `Tauri Production Debug` : `cargo.args = build --release --manifest-path=./src-tauri/Cargo.toml`, `preLaunchTask: ui:build`.
- `tasks.json` : 2 tâches shell, copies fidèles de `examples/tasks.json`.
  - `ui:dev` : `yarn dev`, `isBackground: true`.
  - `ui:build` : `yarn build`.

## Principe (doc)

On contourne la CLI Tauri (`beforeDevCommand` / `beforeBuildCommand` non exécutés) : le serveur dev tourne à part via `preLaunchTask`, et on build avec Cargo direct + `--no-default-features` pour servir le dev-server au lieu des assets disque. Prérequis : extension `vscode-lldb`.

## Points de fidélité

- `tasks.json` garde `yarn dev` / `yarn build` tels que documentés. Pas de variante `pnpm` / `yarn` inventée : la doc de référence n'atteste que `yarn`.
- Route `lldb` : pas de champ `program`. Le binaire `src-tauri/target/debug/mon-app` est le produit du `cargo build` dev, pas un champ à renseigner dans cette route. Le champ `program` (`${workspaceRoot}/src-tauri/target/debug/your-app-name-here.exe`, à adapter en `mon-app.exe`) n'existe que dans la variante Windows `cppvsdbg` de la même page doc — non retenue ici car la consigne demande `lldb`.
- Valeurs hors doc refusées : aucun autre `type` que `lldb` / `cppvsdbg`, aucun flag Cargo hors `--manifest-path` / `--no-default-features` / `--release`.

## Validation

```text
OK /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-dev-quality-workspace/iteration-1/eval-vscode-debug/with_skill/outputs/launch.json: launch.json fidèle (2 configs)
exit=0
```

Commande :

```bash
python3 /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-dev-quality/scripts/check-dev-quality.py --vscode /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-dev-quality-workspace/iteration-1/eval-vscode-debug/with_skill/outputs/launch.json
```

## Sources (commit `ec113a50`, EN canonique seule)

- Fichier : `tauri-docs/src/content/docs/develop/Debug/vscode.mdx` — commit `ec113a50` — titre `Debug in VS Code`.
- Relais skill : `skills/tauri-dev-quality/references/ide-debug.md` (section « VS Code — vscode-lldb, toutes plateformes »), `skills/tauri-dev-quality/examples/launch.json`, `skills/tauri-dev-quality/examples/tasks.json`.
